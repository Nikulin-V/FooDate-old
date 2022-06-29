from django.db import models
from django.utils.safestring import mark_safe
from sorl.thumbnail import get_thumbnail


class PublishedBaseModel(models.Model):
    is_published = models.BooleanField('Опубликовано', default=False)

    class Meta:
        abstract = True


class PhotoBaseModel(models.Model):
    image = models.ImageField(
        upload_to='static/uploads/', null=True, blank=True, verbose_name='Изображение'
    )

    def get_image_x1280(self):
        return get_thumbnail(self.image, '1280', quality=51)

    def get_image_400x300(self):
        return get_thumbnail(self.image, '400x300', crop='center', quality=51)

    def image_tmb(self):
        if self.image:
            return mark_safe(f'<img src="{self.image.url}" width="50"')
        return 'Нет изображения'

    def image_middle(self):
        if self.image:
            return mark_safe(f'<img src="{self.image.url}" width="200"')
        return 'Нет изображения'

    def image_big(self):
        if self.image:
            return mark_safe(f'<img src="{self.image.url}" width="400"')
        return 'Нет изображения'

    image_tmb.short_description = 'Превью'
    image_tmb.allow_tags = True

    class Meta:
        abstract = True
