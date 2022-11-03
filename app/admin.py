from django.contrib import admin

from app.models import Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('slug', 'user', 'product_card')
    list_display_links = ('slug',)
