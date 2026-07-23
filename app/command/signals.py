"""Signal handlers for command image management."""

import logging
import os
from datetime import datetime
from io import BytesIO
from pathlib import Path
from typing import Optional
from uuid import uuid4

from django.apps import apps
from django.core.files.base import ContentFile
from django.db import transaction
from django.db.models.signals import post_delete, post_save, pre_save
from django.dispatch import receiver
from PIL import Image

logger = logging.getLogger("command")

# Constants
THUMBNAIL_SIZE = (300, 300)
THUMBNAIL_QUALITY = 85
DEFAULT_IMAGE_FORMAT = "JPEG"

FORMAT_MAPPING = {
    ".jpg": "JPEG",
    ".jpeg": "JPEG",
    ".png": "PNG",
    ".webp": "WEBP",
    ".gif": "GIF",
}

# Lazy model loading to avoid circular imports
Images = apps.get_model("command", "CommandSectionFeatures")


def generate_unique_filename(original_filename: str) -> str:
    """
    Generate a unique filename with timestamp directory structure.

    Args:
        original_filename: Original file name

    Returns:
        New path with format: YYYY/MM/DD/uuid.ext
    """
    ext = Path(original_filename).suffix.lower()
    new_name = f"{uuid4().hex}{ext}"
    dirname = datetime.now().strftime("%Y/%m/%d")
    result_path = os.path.join(dirname, new_name)
    logger.debug(f"Generated unique filename: {result_path}")
    return result_path


def remove_file_if_exists(file_path: Optional[str]) -> None:
    """
    Safely remove file if it exists.

    Args:
        file_path: Path to the file to remove
    """
    if file_path and os.path.isfile(file_path):
        try:
            os.remove(file_path)
            logger.debug(f"Removed file: {file_path}")
        except OSError as e:
            logger.error(f"Error removing file {file_path}: {e}")


def get_file_path(file_field) -> Optional[str]:
    """Return the storage path for a file field when one is available."""
    if not file_field:
        return None
    try:
        return file_field.path
    except (NotImplementedError, ValueError):
        return None


def queue_file_cleanup(instance, file_path: Optional[str]) -> None:
    """Remember a file path to remove after the model save is committed."""
    if not file_path:
        return

    pending_paths = getattr(instance, "_old_file_paths_to_delete", [])
    if file_path not in pending_paths:
        pending_paths.append(file_path)
        instance._old_file_paths_to_delete = pending_paths


def remove_file_on_commit(file_path: str) -> None:
    """Remove a file only after the surrounding database transaction commits."""
    def cleanup() -> None:
        logger.info(f"Removing old file: {file_path}")
        remove_file_if_exists(file_path)

    transaction.on_commit(cleanup)


def create_thumbnail(image_file, max_size: tuple = THUMBNAIL_SIZE) -> BytesIO:
    """
    Create a thumbnail from an image file.

    Args:
        image_file: Django ImageField file object
        max_size: Maximum dimensions (width, height)

    Returns:
        BytesIO object containing the thumbnail

    Raises:
        ValueError: If image processing fails
    """
    logger.debug(f"Creating thumbnail for image: {image_file.name}")
    try:
        img = Image.open(image_file)
        original_size = img.size
        logger.debug(f"Original image size: {original_size}")

        # Convert RGBA and P mode images to RGB for JPEG compatibility
        if img.mode in ("RGBA", "P", "LA"):
            logger.debug(f"Converting image from {img.mode} to RGB")
            img = img.convert("RGB")

        # Create thumbnail maintaining aspect ratio
        img.thumbnail(max_size, Image.Resampling.LANCZOS)
        logger.debug(f"Thumbnail created with size: {img.size}")

        # Determine image format
        ext = Path(image_file.name).suffix.lower()
        img_format = FORMAT_MAPPING.get(ext, DEFAULT_IMAGE_FORMAT)
        logger.debug(f"Using image format: {img_format}")

        # Save to BytesIO
        thumb_io = BytesIO()
        img.save(thumb_io, format=img_format, quality=THUMBNAIL_QUALITY)
        thumb_io.seek(0)

        logger.info(f"Thumbnail created successfully for {image_file.name}")
        return thumb_io
    except Exception as e:
        logger.error(f"Failed to process image {image_file.name}: {e}", exc_info=True)
        raise ValueError(f"Failed to process image: {str(e)}") from e


def cleanup_old_files(instance, old_instance) -> bool:
    """
    Queue old image and thumbnail files for removal after a successful save.

    Args:
        instance: New model instance
        old_instance: Previous model instance
    """
    logger.debug("Checking old files for deferred cleanup")

    if instance.src and old_instance.src and instance.src == old_instance.src:
        logger.info(f"Old and New image are same: {old_instance.src.name}")
        return False

    # Defer cleanup of the old main image until the database transaction commits.
    if instance.src and old_instance.src and instance.src != old_instance.src:
        old_image_path = get_file_path(old_instance.src)
        logger.debug(f"Queueing old image cleanup: {old_image_path}")
        queue_file_cleanup(instance, old_image_path)

        if old_instance.thumbnail:
            old_thumbnail_path = get_file_path(old_instance.thumbnail)
            logger.debug(f"Queueing old thumbnail cleanup: {old_thumbnail_path}")
            queue_file_cleanup(instance, old_thumbnail_path)
    return True


@receiver(pre_save, sender=Images)
def generate_thumbnail_on_save(sender, instance, **kwargs):
    """
    Generate thumbnail and rename image before saving.

    This signal:
    1. Queues old files for cleanup when image is replaced
    2. Generates a unique filename for the image
    3. Creates a thumbnail from the uploaded image
    4. Saves both with proper naming

    Args:
        sender: The model class (Images)
        instance: The actual instance being saved
        **kwargs: Additional signal arguments
    """

    try:
        # Generate thumbnail if image exists
        if not instance.src:
            logger.debug("No image to process, skipping thumbnail generation")
            return
        if instance.pk:
            old_instance = sender.objects.get(pk=instance.pk)
            if cleanup_old_files(instance, old_instance) is False:
                return
        # Generate unique filename
        original_name = instance.src.name
        instance.src.name = generate_unique_filename(instance.src.name)
        logger.info(f"Renamed image from {original_name} to {instance.src.name}")

        # Create thumbnail
        thumb_io = create_thumbnail(instance.src, THUMBNAIL_SIZE)

        # Save new thumbnail
        thumbnail_name = f"thumb_{Path(instance.src.name).name}"
        instance.thumbnail.save(
            thumbnail_name,
            ContentFile(thumb_io.getvalue()),
            save=False,
        )
        logger.info(f"Thumbnail saved: {thumbnail_name}")

    except Exception as e:
        logger.error(f"Image processing error: {e}", exc_info=True)
        raise ValueError(f"Image processing error: {str(e)}") from e


@receiver(post_save, sender=Images)
def cleanup_old_files_after_save(sender, instance, **kwargs):
    """Remove replaced files only after the model save transaction commits."""
    old_file_paths = getattr(instance, "_old_file_paths_to_delete", [])
    if not old_file_paths:
        return

    for file_path in old_file_paths:
        remove_file_on_commit(file_path)

    instance._old_file_paths_to_delete = []


@receiver(post_delete, sender=Images)
def cleanup_files_on_delete(sender, instance, **kwargs):
    """
    Remove image and thumbnail files when model instance is deleted.

    Args:
        sender: The model class (Images)
        instance: The instance being deleted
        **kwargs: Additional signal arguments
    """
    if sender == Images:
        logger.info(f"Cleaning up files for deleted image (ID: {instance.pk})")
        remove_file_if_exists(get_file_path(instance.src))
        remove_file_if_exists(get_file_path(instance.thumbnail))
        logger.debug("File cleanup completed")
