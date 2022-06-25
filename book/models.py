from django.core import validators
from django.db import models
from tinymce.models import HTMLField

from core.choices import TEMPERATURE_UNITS, ENERGY_UNITS
from core.models import PublishedBaseModel


class ProductCategoryManager(models.Manager):
    pass


class ProductCategory(models.Model):
    categories = ProductCategoryManager()

    name = models.CharField('Название', max_length=255)
    slug = models.CharField(max_length=255, validators=[validators.validate_slug])

    def __str__(self):
        return self.slug[:15]

    class Meta:
        verbose_name = 'Категория продуктов'
        verbose_name_plural = 'Категории продуктов'


class ProductSubcategoryManager(models.Manager):
    pass


class ProductSubcategory(models.Model):
    subcategories = ProductSubcategoryManager()

    name = models.CharField('Название', max_length=255)
    slug = models.CharField(max_length=255, validators=[validators.validate_slug])

    def __str__(self):
        return self.slug[:15]

    class Meta:
        verbose_name = 'Подкатегория продуктов'
        verbose_name_plural = 'Подкатегории продуктов'


class ProductCardManager(models.Manager):
    def get_published(self):
        self.get_queryset().filter(is_published=True)


class ProductCard(PublishedBaseModel):
    cards = ProductCardManager()

    title = models.CharField('Название', max_length=255)
    name = models.CharField('Наименование', max_length=255, null=True)
    slug = models.CharField(max_length=255, validators=[validators.validate_slug], null=True)
    category = models.ForeignKey(ProductCategory, on_delete=models.SET_NULL, null=True,
                                 related_name='products', verbose_name='Категория продуктов')
    subcategory = models.ForeignKey(ProductSubcategory, on_delete=models.SET_NULL, null=True,
                                    related_name='products', verbose_name='Подкатегория продуктов')
    shelf_life = models.DurationField('Срок годности', null=True)
    shelf_life_after_opening = models.DurationField('Срок годности', null=True)
    storage_temperature = models.FloatField('Температура хранения', null=True)
    storage_temperature_unit = models.CharField('Единица измерения температуры хранения',
                                                choices=TEMPERATURE_UNITS, null=True, max_length=3)
    composition = models.CharField('Состав', max_length=1023, null=True)
    energy_value = models.FloatField('Энергетическая ценность', null=True,
                                     validators=[validators.MinValueValidator(0)])
    energy_value_unit = models.CharField('Единица измерения энергетической ценности', max_length=4,
                                         choices=ENERGY_UNITS, null=True)

    def __str__(self):
        return self.slug[:15]

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'


class RecipeCategoryManager(models.Manager):
    pass


class RecipeCategory(models.Model):
    categories = RecipeCategoryManager()

    name = models.CharField('Название', max_length=255)
    slug = models.CharField(max_length=255, validators=[validators.validate_slug])

    def __str__(self):
        return self.slug[:15]

    class Meta:
        verbose_name = 'Категория рецептов'
        verbose_name_plural = 'Категории рецептов'


class RecipeManager(models.Manager):
    def get_published(self):
        self.get_queryset().filter(is_published=True)


class Recipe(PublishedBaseModel):
    recipes = RecipeManager()

    name = models.CharField('Название', max_length=255)
    slug = models.CharField(max_length=255, validators=[validators.validate_slug], null=True)
    category = models.ForeignKey(RecipeCategory, on_delete=models.SET_NULL, null=True,
                                 related_name='products', verbose_name='Категория рецептов')
    people_count = models.IntegerField('Кол-во человек', default=1,
                                       help_text='Количество человек, на которое рассчитано блюдо')
    ingredients = HTMLField('Ингредиенты',
                            help_text='Напишите список ингредиентов и сколько их понадобится')
    products = models.ManyToManyField(ProductCard,
                                      verbose_name='Продукты для рецепта',
                                      related_name='recipes')
    energy_value = models.FloatField('Энергетическая ценность', null=True,
                                     validators=[validators.MinValueValidator(0)])
    energy_value_unit = models.CharField('Единица измерения энергетической ценности', max_length=4,
                                         choices=ENERGY_UNITS, null=True)

    def __str__(self):
        return self.slug[:15]

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
