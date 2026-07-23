import os
from io import BytesIO
from tempfile import TemporaryDirectory

from django.core.files.uploadedfile import SimpleUploadedFile
from django.db import transaction
from django.test import TransactionTestCase, override_settings
from PIL import Image

from .models import CommandSection, CommandSectionFeatures


def make_image_upload(filename="trainer.jpg"):
    image_io = BytesIO()
    Image.new("RGB", (20, 20), color="red").save(image_io, format="JPEG")
    image_io.seek(0)
    return SimpleUploadedFile(filename, image_io.read(), content_type="image/jpeg")


class CommandImageCleanupTests(TransactionTestCase):
    def setUp(self):
        self.media_root = TemporaryDirectory()
        self.override = override_settings(MEDIA_ROOT=self.media_root.name)
        self.override.enable()
        self.addCleanup(self.override.disable)
        self.addCleanup(self.media_root.cleanup)

        self.section = CommandSection.objects.create(
            title="Команда",
            desc="Описание",
            slug="team",
        )

    def create_feature(self):
        return CommandSectionFeatures.objects.create(
            section=self.section,
            name="Тренер",
            src=make_image_upload("old.jpg"),
        )

    def test_old_files_are_kept_when_transaction_rolls_back(self):
        feature = self.create_feature()
        old_src_path = feature.src.path
        old_thumbnail_path = feature.thumbnail.path

        with self.assertRaises(RuntimeError):
            with transaction.atomic():
                feature.src = make_image_upload("new.jpg")
                feature.save()
                raise RuntimeError("rollback")

        self.assertTrue(os.path.exists(old_src_path))
        self.assertTrue(os.path.exists(old_thumbnail_path))

    def test_old_files_are_removed_after_successful_commit(self):
        feature = self.create_feature()
        old_src_path = feature.src.path
        old_thumbnail_path = feature.thumbnail.path

        with transaction.atomic():
            feature.src = make_image_upload("new.jpg")
            feature.save()

        self.assertFalse(os.path.exists(old_src_path))
        self.assertFalse(os.path.exists(old_thumbnail_path))
