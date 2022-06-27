from django.contrib import admin

from book.models import ProductCategory, ProductSubcategory, ProductCard, RecipeCategory, Recipe


@admin.register(ProductCategory)
class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    list_editable = ('slug',)
    list_display_links = ('name',)


@admin.register(ProductSubcategory)
class ProductSubcategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    list_editable = ('slug',)
    list_display_links = ('name',)


@admin.register(ProductCard)
class ProductCardAdmin(admin.ModelAdmin):
    list_display = ('slug', 'title', 'name', 'is_published')
    list_editable = ('is_published',)
    list_display_links = ('slug',)


@admin.register(RecipeCategory)
class RecipeCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    list_editable = ('slug',)
    list_display_links = ('name',)


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('slug', 'name', 'is_published')
    list_editable = ('is_published',)
    list_display_links = ('name',)
