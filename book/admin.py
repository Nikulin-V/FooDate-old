from django.contrib import admin

from book.models import (
    ProductCategory,
    ProductSubcategory,
    ProductCard,
    RecipeCategory,
    Recipe,
    ProductPhoto,
    RecipePhoto,
)


@admin.register(ProductCategory)
class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    list_editable = ('slug',)
    list_display_links = ('name',)
    search_fields = ('name',)


@admin.register(ProductSubcategory)
class ProductSubcategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    list_editable = ('slug',)
    list_display_links = ('name',)
    search_fields = ('name',)


class ProductGalleryInlined(admin.TabularInline):
    model = ProductPhoto
    can_delete = False


@admin.register(ProductCard)
class ProductCardAdmin(admin.ModelAdmin):
    list_display = ('slug', 'name', 'designation', 'image_tmb', 'is_published')
    list_editable = ('is_published',)
    list_display_links = ('slug',)
    exclude = ('gallery',)
    inlines = (ProductGalleryInlined,)
    readonly_fields = ('image_tmb',)
    search_fields = ('name',)


@admin.register(RecipeCategory)
class RecipeCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    list_editable = ('slug',)
    list_display_links = ('name',)
    search_fields = ('name',)


class RecipeGalleryInlined(admin.TabularInline):
    model = RecipePhoto
    can_delete = False


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('slug', 'name', 'is_published')
    list_editable = ('is_published',)
    list_display_links = ('name',)
    exclude = ('gallery',)
    inlines = (RecipeGalleryInlined,)
    search_fields = ('name',)
