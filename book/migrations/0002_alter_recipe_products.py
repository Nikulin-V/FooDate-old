# Generated by Django 4.0.5 on 2022-08-25 13:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='products',
            field=models.ManyToManyField(blank=True, related_name='recipes', to='book.productcard', verbose_name='Продукты, необходимые для приготовления'),
        ),
    ]
