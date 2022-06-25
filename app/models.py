from datetime import datetime

from django.core import validators
from django.db import models

from book.models import ProductCard
from core.choices import AMOUNT_UNIT


class ProductManager(models.Manager):
    pass


class Product(ProductCard):
    products = ProductManager()

    amount = models.FloatField('Количество продукта', null=True)
    amount_unit = models.CharField('Единица измерения количества продукта',
                                   choices=AMOUNT_UNIT, null=True, max_length=2)
    production_date = models.DateTimeField('Дата изготовления', null=True,
                                           validators=[
                                               validators.MaxValueValidator(datetime.now())
                                           ])
    purchase_date = models.DateTimeField('Дата покупки', null=True,
                                         validators=[
                                             validators.MaxValueValidator(datetime.now())
                                         ])
