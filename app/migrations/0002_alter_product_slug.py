# Generated by Django 4.0.5 on 2022-06-30 13:50

import django.core.validators
from django.db import migrations, models
import re


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='slug',
            field=models.CharField(max_length=255, unique=True, validators=[django.core.validators.RegexValidator(re.compile('^[-a-zA-Z0-9_]+\\Z'), 'Enter a valid “slug” consisting of letters, numbers, underscores or hyphens.', 'invalid')]),
        ),
    ]
