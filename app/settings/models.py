import logging

from django.db import models

logger = logging.getLogger("settings")

        
class Landing(models.Model):
    """Global Landing settings and configuration."""

    avatar = models.ImageField(blank=True)
    title = models.CharField(max_length=250, unique=True)
    desc = models.CharField(
        max_length=250, unique=True, verbose_name="Landing Description"
    )
    footer = models.CharField(max_length=250, unique=True)

    class Meta:
        verbose_name = "Landing Settings"
        verbose_name_plural = "Landing Settings"

    def __str__(self):
        return self.title

    def __repr__(self):
        return f"<LandingSettings: {self.title}>"

class SocialMedia(models.Model):
    """Social media links associated with Landing settings."""

    SOCIAL_MEDIA_TYPE_CHOICES = [
        ("fa-vk", "VK"),
        ("fa-linkedin", "LinkedIn"),
        ("fa-google", "Google"),
        ("fa-stack-overflow", "Stack Overflow"),
        ("fa-github", "GitHub"),
        ("fa-youtube", "YouTube"),
    ]

    title = models.CharField(
        max_length=250,
        choices=SOCIAL_MEDIA_TYPE_CHOICES,
        default="fa-vk",
        verbose_name="Social Media",
    )
    url_link = models.URLField(max_length=250, verbose_name="URL")
    settings = models.ForeignKey(
        Landing, 
        on_delete=models.CASCADE, 
        related_name="social_media",         
        null=False,
        blank=False
    )

    class Meta:
        verbose_name = "Social Media"
        verbose_name_plural = "Social Media"

    def __str__(self):
        return self.title

    def __repr__(self):
        return f"<SocialMedia: {self.title} - {self.url_link}>"
