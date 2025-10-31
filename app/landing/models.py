from django.db import models
from django.utils.text import slugify

class Page(models.Model):
    title = models.CharField(max_length=200, verbose_name="Название страницы")
    slug = models.SlugField(max_length=200, unique=True, verbose_name="URL")
    meta_title = models.CharField(max_length=200, blank=True, verbose_name="Meta title")
    meta_description = models.TextField(blank=True, verbose_name="Meta description")
    is_active = models.BooleanField(default=True, verbose_name="Активная")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Страница"
        verbose_name_plural = "Страницы"

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)


class BlockType(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название блока")
    template = models.CharField(max_length=200, verbose_name="Шаблон")
    description = models.TextField(blank=True, verbose_name="Описание")

    class Meta:
        verbose_name = "Тип блока"
        verbose_name_plural = "Типы блоков"

    def __str__(self):
        return self.name


class Block(models.Model):
    page = models.ForeignKey(Page, on_delete=models.CASCADE, related_name='blocks', verbose_name="Страница")
    block_type = models.ForeignKey(BlockType, on_delete=models.CASCADE, verbose_name="Тип блока")
    title = models.CharField(max_length=200, blank=True, verbose_name="Заголовок")
    content = models.TextField(blank=True, verbose_name="Содержание")
    image = models.ImageField(upload_to='blocks/', blank=True, null=True, verbose_name="Изображение")
    button_text = models.CharField(max_length=50, blank=True, verbose_name="Текст кнопки")
    button_url = models.CharField(max_length=200, blank=True, verbose_name="URL кнопки")
    order = models.IntegerField(default=0, verbose_name="Порядок")
    is_active = models.BooleanField(default=True, verbose_name="Активный")
    
    # Дополнительные поля для гибкости
    background_color = models.CharField(max_length=7, default='#ffffff', verbose_name="Цвет фона")
    text_color = models.CharField(max_length=7, default='#000000', verbose_name="Цвет текста")
    custom_css = models.TextField(blank=True, verbose_name="Пользовательский CSS")
    
    class Meta:
        verbose_name = "Блок"
        verbose_name_plural = "Блоки"
        ordering = ['order']

    def __str__(self):
        return f"{self.page.title} - {self.block_type.name}"
    
class Images(models.Model):
    IMAGE_TYPE_CHOICES = [
        ("main", "Основное изображение"),
        ("secondary", "Дополнительное"),
        ("thumbnail", "Миниатюра"),
    ]

    image = models.ImageField(blank=True)
    thumbnail = models.ImageField(upload_to="%Y/%m/%d/thumbnails", blank=True, null=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="images")

    image_type = models.CharField(
        max_length=10,
        choices=IMAGE_TYPE_CHOICES,
        default="secondary",
        verbose_name="Тип изображения",
    )