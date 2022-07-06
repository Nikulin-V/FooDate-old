from datetime import datetime

from django.contrib.auth import get_user_model
from django.core import validators
from django.db import models
# noinspection PyPackageRequirements
from slugify import slugify

from book.models import ProductCard
from core.choices import AMOUNT_UNIT
from core.middleware import get_user

User = get_user_model()


class ProductManager(models.Manager):
    pass


class Product(models.Model):
    products = ProductManager()

    user = models.ForeignKey(User, on_delete=models.CASCADE, default=get_user)
    slug = models.CharField(max_length=255, validators=[validators.validate_slug], unique=True,
                            blank=True, null=True)
    product_card = models.ForeignKey(
        ProductCard, on_delete=models.DO_NOTHING, related_name='products'
    )
    amount = models.FloatField('Количество продукта', null=True, blank=True)
    amount_unit = models.CharField('Единица измерения количества продукта', choices=AMOUNT_UNIT,
                                   default=AMOUNT_UNIT[1], null=True, blank=True, max_length=2)
    production_date = models.DateTimeField('Дата изготовления', null=True, blank=True,
                                           validators=[validators.MaxValueValidator(datetime.now)])
    purchase_date = models.DateTimeField('Дата покупки', null=True, blank=True,
                                         validators=[validators.MaxValueValidator(datetime.now)])

    def save(self, *args, **kwargs):
        super(Product, self).save(*args, **kwargs)
        self.slug = slugify(f'{self.product_card.name} {self.pk}')
        super(Product, self).save(*args, **kwargs)

    def __str__(self):
        return f'<Product> {self.pk} | {self.product_card.slug} {self.amount} {self.amount_unit}'

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'
