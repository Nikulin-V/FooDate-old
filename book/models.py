from django.core import validators
from django.db import models
from django.utils.safestring import mark_safe
from tinymce.models import HTMLField

from core.choices import TEMPERATURE_UNITS, ENERGY_UNITS
from core.models import PublishedBaseModel, PhotoBaseModel, NameSlugBaseModel


class ProductCategoryManager(models.Manager):
    pass


class ProductCategory(NameSlugBaseModel):
    categories = ProductCategoryManager()

    name = models.CharField('Название', max_length=255, unique=True)
    slug = models.CharField(max_length=255, unique=True, validators=[validators.validate_slug],
                            null=True, blank=True)

    class Meta:
        verbose_name = 'Категорию продуктов'
        verbose_name_plural = 'Категории продуктов'


class ProductSubcategoryManager(models.Manager):
    pass


class ProductSubcategory(NameSlugBaseModel):
    subcategories = ProductSubcategoryManager()

    name = models.CharField('Название', max_length=255, unique=True)
    slug = models.CharField(max_length=255, unique=True, validators=[validators.validate_slug],
                            null=True, blank=True)
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE, null=True,
                                 related_name='subcategories', verbose_name='Категория продуктов')

    def __str__(self):
        return self.name[:50]

    class Meta:
        verbose_name = 'Подкатегорию продуктов'
        verbose_name_plural = 'Подкатегории продуктов'


class ProductCardManager(models.Manager):
    def get_published(self):
        self.get_queryset().filter(is_published=True)


class ProductCard(NameSlugBaseModel, PublishedBaseModel, PhotoBaseModel):
    cards = ProductCardManager()

    name = models.CharField('Название', max_length=255, unique=True)
    slug = models.CharField(max_length=255, unique=True, validators=[validators.validate_slug],
                            null=True, blank=True)
    designation = models.CharField('Наименование', max_length=255)
    subcategory = models.ForeignKey(
        ProductSubcategory,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='products',
        verbose_name='Подкатегория продуктов',
    )
    shelf_life = models.DurationField(
        'Срок годности',
        null=True,
        blank=True,
        help_text='Период времени в формате (дни часы:минуты:секунды)',
    )
    shelf_life_after_opening = models.DurationField(
        'Срок годности после вскрытия',
        null=True,
        blank=True,
        help_text='Период времени в формате (дни часы:минуты:секунды)',
    )
    min_storage_temperature = models.FloatField('Минимальная температура хранения', null=True,
                                                blank=True)
    min_storage_temperature_unit = models.CharField(
        'Единица измерения минимальной температуры хранения',
        choices=TEMPERATURE_UNITS,
        null=True,
        blank=True,
        max_length=3,
    )
    max_storage_temperature = models.FloatField('Максимальная температура хранения', null=True,
                                                blank=True)
    max_storage_temperature_unit = models.CharField(
        'Единица измерения максимальной температуры хранения',
        choices=TEMPERATURE_UNITS,
        null=True,
        blank=True,
        max_length=3,
    )
    composition = models.TextField('Состав', max_length=1023, null=True, blank=True)
    energy_value = models.FloatField(
        'Энергетическая ценность',
        null=True,
        blank=True,
        help_text='Энергетическая ценность на 100 грамм продукта',
        validators=[validators.MinValueValidator(0)],
    )
    energy_value_unit = models.CharField(
        'Единица измерения энергетической ценности',
        choices=ENERGY_UNITS,
        null=True,
        blank=True,
        max_length=4,
    )
    proteins = models.FloatField(
        'Белки (в граммах)', null=True, blank=True, validators=[validators.MinValueValidator(0)]
    )
    fats = models.FloatField(
        'Жиры (в граммах)', null=True, blank=True, validators=[validators.MinValueValidator(0)]
    )
    carbohydrates = models.FloatField(
        'Углеводы (в граммах)', null=True, blank=True, validators=[validators.MinValueValidator(0)]
    )
    image = models.ImageField(
        upload_to='static/uploads/products/images',
        null=True,
        blank=True,
        verbose_name='Изображение продукта',
    )
    gallery = models.ManyToManyField(
        'book.ProductPhoto', verbose_name='Фотографии', related_name='products'
    )

    class Meta:
        verbose_name = 'Карточку продукта'
        verbose_name_plural = 'Карточки продуктов'


class ProductPhoto(PublishedBaseModel):
    upload = models.ImageField(upload_to='static/uploads/products/gallery', null=True, blank=True)
    product = models.ForeignKey(ProductCard, verbose_name='Продукт', on_delete=models.CASCADE)

    def image(self):
        return mark_safe(f'<img src="{self.upload.url}" width="200"')

    class Meta:
        verbose_name = 'Изображение продукта'
        verbose_name_plural = 'Изображения продукта'


class RecipeCategoryManager(models.Manager):
    pass


class RecipeCategory(models.Model):
    categories = RecipeCategoryManager()

    name = models.CharField('Название', max_length=255, unique=True)
    slug = models.CharField(max_length=255, unique=True, validators=[validators.validate_slug],
                            null=True, blank=True)

    class Meta:
        verbose_name = 'Категорию рецептов'
        verbose_name_plural = 'Категории рецептов'


class RecipeManager(models.Manager):
    def get_published(self):
        self.get_queryset().filter(is_published=True)


class Recipe(PublishedBaseModel, PhotoBaseModel):
    recipes = RecipeManager()

    name = models.CharField('Название', max_length=255, unique=True)
    slug = models.CharField(max_length=255, unique=True, validators=[validators.validate_slug],
                            null=True, blank=True)
    category = models.ForeignKey(
        RecipeCategory,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='recipes',
        verbose_name='Категория рецептов',
    )
    people_count = models.IntegerField(
        'Кол-во человек', default=1, help_text='Количество человек, на которое рассчитано блюдо'
    )
    recipe = HTMLField('Рецепт', help_text='Подробно опишите процесс приготовления по шагам')
    products = models.ManyToManyField(
        ProductCard, verbose_name='Продукты, необходимые для приготовления', related_name='recipes'
    )
    energy_value = models.FloatField(
        'Энергетическая ценность',
        null=True,
        blank=True,
        validators=[validators.MinValueValidator(0)],
    )
    energy_value_unit = models.CharField(
        'Единица измерения энергетической ценности',
        max_length=4,
        choices=ENERGY_UNITS,
        null=True,
        blank=True,
    )
    image = models.ImageField(
        upload_to='static/uploads/recipes/images',
        null=True,
        blank=True,
        verbose_name='Изображение блюда',
    )
    gallery = models.ManyToManyField(
        'book.RecipePhoto', verbose_name='Фотографии', related_name='products'
    )

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'


class RecipePhoto(PublishedBaseModel):
    upload = models.ImageField(upload_to='static/uploads/recipes/gallery', null=True, blank=True)
    recipe = models.ForeignKey(Recipe, verbose_name='Рецепт', on_delete=models.CASCADE)

    def image(self):
        return mark_safe(f'<img src="{self.upload.url}" width="200"')

    class Meta:
        verbose_name = 'Изображение блюда'
        verbose_name_plural = 'Изображения блюда'
