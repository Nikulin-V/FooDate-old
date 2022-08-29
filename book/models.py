from django.core import validators
from django.db import models
from django.db.models import Q
from django.utils.safestring import mark_safe
# noinspection PyPackageRequirements
from slugify import slugify
from tinymce.models import HTMLField

import core.validators
from core.choices import TEMPERATURE_UNITS, ENERGY_UNITS
from core.models import PublishedBaseModel, PhotoBaseModel, NameSlugBaseModel


class ProductCategoryManager(models.Manager):
    def get_active(self):
        """Returns dictionary with category if it has active subcategories as key and its subcategories"""
        active_categories = (
            self.get_queryset()
            .filter(subcategories__product_cards__is_published=True)
        )
        return {
            category: set(ProductSubcategory.subcategories.get_active(category))
            for category in active_categories
        }


class ProductCategory(NameSlugBaseModel):
    """Category of products subcategories"""

    categories = ProductCategoryManager()

    name = models.CharField('Название', max_length=255, unique=True)
    slug = models.CharField(max_length=255, unique=True, validators=[validators.validate_slug],
                            null=True, blank=True)

    class Meta:
        verbose_name = 'Категорию продуктов'
        verbose_name_plural = 'Категории продуктов'


class ProductSubcategoryManager(models.Manager):
    def get_active(self, category):
        """Returns list with subcategories from category with published ProductCards"""
        return set(self.get_queryset().filter(category=category, product_cards__is_published=True))


class ProductSubcategory(NameSlugBaseModel):
    """Subcategory of product cards"""

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
        """Returns published product cards"""
        return self.get_queryset().filter(is_published=True)

    def search(self, search):
        """
        Returns product cards based on search string

        :param search: search string
        :return: QuerySet of Product cards
        """
        return self.get_published().filter(
            Q(name__iregex=search) or Q(slug__iregex=search) or
            Q(designation__iregex=search) or Q(subcategory__category__name__iregex=search)
            or Q(subcategory__name__iregex=search)
        )


class ProductCard(NameSlugBaseModel, PublishedBaseModel, PhotoBaseModel):
    """Model of product card which contains info about product"""

    cards = ProductCardManager()

    designation = models.CharField('Наименование', max_length=255)
    subcategory = models.ForeignKey(
        ProductSubcategory,
        on_delete=models.DO_NOTHING,
        related_name='product_cards',
        verbose_name='Подкатегория продуктов'
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
    max_storage_temperature = models.FloatField('Максимальная температура хранения', null=True,
                                                blank=True)
    storage_temperature_unit = models.CharField(
        'Единица измерения температуры хранения',
        choices=TEMPERATURE_UNITS,
        default=TEMPERATURE_UNITS[0],
        max_length=3,
    )
    composition = models.TextField('Состав', max_length=1023, null=True, blank=True)
    energy_value = models.FloatField(
        'Энергетическая ценность',
        null=True,
        blank=True,
        help_text='Энергетическая ценность на 100 грамм продукта',
        validators=[
            core.validators.BiggerThanValidator(0)
        ]
    )
    energy_value_unit = models.CharField(
        'Единица измерения энергетической ценности',
        choices=ENERGY_UNITS,
        default=ENERGY_UNITS[0],
        max_length=4,
    )
    proteins = models.FloatField(
        'Белки (в граммах)', null=True, blank=True, validators=[
            core.validators.BiggerThanValidator(0)
        ]
    )
    fats = models.FloatField(
        'Жиры (в граммах)', null=True, blank=True, validators=[
            core.validators.BiggerThanValidator(0)
        ]
    )
    carbohydrates = models.FloatField(
        'Углеводы (в граммах)', null=True, blank=True, validators=[
            core.validators.BiggerThanValidator(0)
        ]
    )
    image = models.ImageField(
        upload_to='products/images',
        null=True,
        blank=True,
        verbose_name='Изображение продукта',
    )
    gallery = models.ManyToManyField(
        'book.ProductPhoto', verbose_name='Фотографии', related_name='product_cards'
    )

    def save(self, *args, **kwargs):
        if self.image.name:
            if '/' not in self.image.name:
                change_image_name(self.name, self.image)

        if not self.subcategory:
            super(ProductCard, self).save(*args, **kwargs)
            self.subcategory, has_category = ProductSubcategory.subcategories.get_or_create(
                name='Другое',
            )
            if not has_category:
                self.subcategory.category = ProductCategory.categories.get_or_create(
                    name='Другое',
                )[0]

        super(ProductCard, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'Карточку продукта'
        verbose_name_plural = 'Карточки продуктов'


class ProductPhoto(PublishedBaseModel):
    """Model of product photo"""

    upload = models.ImageField(upload_to='products/gallery', null=True, blank=True)
    product = models.ForeignKey(ProductCard, verbose_name='Продукт', on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        if self.upload.name:
            if '/' not in self.upload.name:
                change_image_name(self.product.name, self.upload)
        super(ProductPhoto, self).save()

    def image(self):
        return mark_safe(f'<img src="{self.upload.url}" width="200"')

    class Meta:
        verbose_name = 'Изображение продукта'
        verbose_name_plural = 'Изображения продукта'


class RecipeCategoryManager(models.Manager):
    pass


class RecipeCategory(models.Model):
    """Category of recipes"""

    categories = RecipeCategoryManager()

    name = models.CharField('Название', max_length=255, unique=True)
    slug = models.CharField(max_length=255, unique=True, validators=[validators.validate_slug],
                            null=True, blank=True)

    class Meta:
        verbose_name = 'Категорию рецептов'
        verbose_name_plural = 'Категории рецептов'


class RecipeManager(models.Manager):
    def get_published(self):
        """Returns published recipes"""
        self.get_queryset().filter(is_published=True)


class Recipe(PublishedBaseModel, PhotoBaseModel):
    """Model of recipe which contains info about recipe"""

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
        'Кол-во человек', default=1, help_text='Количество человек, на которое рассчитано блюдо',
        validators=[validators.MinValueValidator(1)]
    )
    recipe = HTMLField('Рецепт', help_text='Подробно опишите процесс приготовления по шагам')
    products = models.ManyToManyField(
        ProductCard, verbose_name='Продукты, необходимые для приготовления', related_name='recipes'
    )
    energy_value = models.FloatField(
        'Энергетическая ценность',
        null=True,
        blank=True,
        validators=[
            core.validators.BiggerThanValidator(0)
        ]
    )
    energy_value_unit = models.CharField(
        'Единица измерения энергетической ценности',
        max_length=4,
        choices=ENERGY_UNITS,
        null=True,
        blank=True,
    )
    image = models.ImageField(
        upload_to='recipes/images',
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
    """Model of recipe photo"""

    upload = models.ImageField(upload_to='recipes/gallery', null=True, blank=True)
    recipe = models.ForeignKey(Recipe, verbose_name='Рецепт', on_delete=models.CASCADE)

    def image(self):
        return mark_safe(f'<img src="{self.upload.url}" width="200"')

    class Meta:
        verbose_name = 'Изображение блюда'
        verbose_name_plural = 'Изображения блюда'


def change_image_name(name, image):
    """Changes image name to its slug"""

    slug = slugify(name)
    name_split = image.name.split('.')
    path, extension = '.'.join(name_split)[:-1], name_split[-1]
    path = path.split('/')[:-1]
    extension = image.name.split('.')[-1]
    path.append('.'.join((slug, extension)))
    image.name = '/'.join(path)
