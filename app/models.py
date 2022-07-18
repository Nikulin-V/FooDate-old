from uuid import uuid4

from django.contrib.auth import get_user_model
from django.core import validators
from django.db import models

from book.models import ProductCard
from core.choices import AMOUNT_UNIT
from core.middleware import get_user
import core.validators

User = get_user_model()


class ProductManager(models.Manager):
    pass


class Product(models.Model):
    products = ProductManager()

    user = models.ForeignKey(User, on_delete=models.CASCADE, default=get_user)
    slug = models.CharField(max_length=255, validators=[validators.validate_slug],
                            null=True, blank=True)
    product_card = models.ForeignKey(
        ProductCard, on_delete=models.DO_NOTHING, related_name='products'
    )
    amount = models.FloatField('Количество продукта', null=True, blank=True, validators=[
        core.validators.BiggerThanValidator(0)
    ])
    amount_unit = models.CharField('Единица измерения количества продукта', choices=AMOUNT_UNIT,
                                   default=AMOUNT_UNIT[1], null=True, blank=True, max_length=2)
    production_date = models.DateTimeField('Дата изготовления', null=True, blank=True,
                                           validators=[core.validators.date_in_past])
    purchase_date = models.DateTimeField('Дата покупки', null=True, blank=True,
                                         validators=[core.validators.date_in_past])

    def save(self, *args, **kwargs):
        self.slug = f'product-{uuid4()}'
        super(Product, self).save()

    def __str__(self):
        return self.slug

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'
