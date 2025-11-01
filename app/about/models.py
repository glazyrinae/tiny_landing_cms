from django.db import models
from django.utils.text import slugify

class AboutSection(models.Model):
    title = models.CharField(max_length=200, blank=False, verbose_name="Заголовок блока")
    desc = models.TextField(max_length=800, blank=False,  verbose_name="Описание блока")
    slug = models.SlugField(max_length=250, verbose_name="Ссылка на блок")
    is_active = models.BooleanField(default=True, verbose_name="Видимость")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'section_about_main' 
        verbose_name = "Блок о нас"
        verbose_name_plural = "Блок о нас"

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

class AboutSectionFeatures(models.Model):
    title = models.CharField(max_length=100, blank=True,  verbose_name="Доп.информация")
    css_class = models.CharField(max_length=100, blank=True,  verbose_name="css-стили")
    is_active = models.BooleanField(default=True, verbose_name="Видимость")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    section = models.ForeignKey(AboutSection, on_delete=models.CASCADE, related_name="features")
    
    class Meta:
        db_table = 'section_about_features' 

class AboutSectionWidget(models.Model):
    html_content = models.TextField(max_length=800, blank=True,  verbose_name="Виджет")
    is_active = models.BooleanField(default=True, verbose_name="Видимость")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    section = models.ForeignKey(AboutSection, on_delete=models.CASCADE, related_name="widget")

    class Meta:
        db_table = 'section_about_widget' 

class AboutSectionImages(models.Model):
    src = models.ImageField(blank=True)
    section = models.ForeignKey(AboutSection, on_delete=models.CASCADE, related_name="images")
    thumbnail = models.ImageField(upload_to="%Y/%m/%d/thumbnails", blank=True, null=True)
    alt = models.CharField(max_length=100, blank=True,  verbose_name="Описание картинки")

    class Meta:
        db_table = 'section_about_images'
        verbose_name = "Изображение"
        verbose_name_plural = "Изображения"