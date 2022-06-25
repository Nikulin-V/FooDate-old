from django.db import models


class PublishedBaseModel(models.Model):
    is_published = models.BooleanField('Опубликовано', default=False)

    class Meta:
        abstract = True
