from django.contrib import admin
from .models import Product, Category, Brand, Shop


@admin.register(Product)
class DealAdmin(admin.ModelAdmin):
    list_display = ['name']
    list_filter = ['category']


@admin.register(Category)
class DealAdmin(admin.ModelAdmin):
    list_display = ['name']
    readonly_fields = ['slug']


@admin.register(Brand)
class DealAdmin(admin.ModelAdmin):
    list_display = ['name']
    readonly_fields = ['slug']


@admin.register(Shop)
class DealAdmin(admin.ModelAdmin):
    list_display = ['name']
