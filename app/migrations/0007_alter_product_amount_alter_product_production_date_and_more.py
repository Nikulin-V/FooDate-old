# Generated by Django 4.0.5 on 2022-07-06 17:13

import core.validators
import django.core.validators
from django.db import migrations, models
import re


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_alter_product_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='amount',
            field=models.FloatField(blank=True, null=True, validators=[core.validators.BiggerThanValidator(0)], verbose_name='Количество продукта'),
        ),
        migrations.AlterField(
            model_name='product',
            name='production_date',
            field=models.DateTimeField(blank=True, null=True, validators=[core.validators.date_in_past], verbose_name='Дата изготовления'),
        ),
        migrations.AlterField(
            model_name='product',
            name='purchase_date',
            field=models.DateTimeField(blank=True, null=True, validators=[core.validators.date_in_past], verbose_name='Дата покупки'),
        ),
        migrations.AlterField(
            model_name='product',
            name='slug',
            field=models.CharField(default='product-fe1e56bf-2b47-4a52-a6f3-d810b3c50e93', max_length=255, validators=[django.core.validators.RegexValidator(re.compile('^[-a-zA-Z0-9_]+\\Z'), 'Enter a valid “slug” consisting of letters, numbers, underscores or hyphens.', 'invalid')]),
        ),
    ]
