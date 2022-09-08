from django.core import validators
from django.db import models
from django.utils.safestring import mark_safe
# noinspection PyPackageRequirements
from slugify import slugify
from sorl.thumbnail import get_thumbnail


class NameSlugBaseModel(models.Model):
    """Abstract model which saves its slug from its name"""

    name = models.CharField('Название', max_length=255, unique=True)
    slug = models.CharField(max_length=255, unique=True, validators=[validators.validate_slug],
                            blank=True, null=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(NameSlugBaseModel, self).save(*args, **kwargs)

    def __str__(self):
        return self.name[:50]

    class Meta:
        abstract = True


class PublishedBaseModel(models.Model):
    """Abstract model which allows to publish/not to publish itself"""

    is_published = models.BooleanField('Опубликовано', default=False)

    class Meta:
        abstract = True


class PhotoBaseModel(models.Model):
    """Abstract model of photo"""

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
