# Generated by Django 4.0.5 on 2022-08-25 12:29

import core.middleware
import core.validators
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.db.models.manager
import re


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('book', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.CharField(blank=True, max_length=255, null=True, validators=[django.core.validators.RegexValidator(re.compile('^[-a-zA-Z0-9_]+\\Z'), 'Enter a valid “slug” consisting of letters, numbers, underscores or hyphens.', 'invalid')])),
                ('amount', models.FloatField(blank=True, null=True, validators=[core.validators.BiggerThanValidator(0)], verbose_name='Количество продукта')),
                ('amount_unit', models.CharField(blank=True, choices=[('мг', 'миллиграммы'), ('г', 'граммы'), ('кг', 'килограммы'), ('мл', 'миллилитры'), ('л', 'литры')], default=('г', 'граммы'), max_length=2, null=True, verbose_name='Единица измерения количества продукта')),
                ('production_date', models.DateTimeField(blank=True, null=True, validators=[core.validators.date_in_past], verbose_name='Дата изготовления')),
                ('purchase_date', models.DateTimeField(blank=True, null=True, validators=[core.validators.date_in_past], verbose_name='Дата покупки')),
                ('product_card', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='products', to='book.productcard')),
                ('user', models.ForeignKey(default=core.middleware.get_user, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Продукт',
                'verbose_name_plural': 'Продукты',
            },
            managers=[
                ('products', django.db.models.manager.Manager()),
            ],
        ),
    ]
