from django.contrib import admin
from .models import Sneaker, Brand, Category


@admin.register(Sneaker)
class SneakerAdmin(admin.ModelAdmin):
    """Админ панель Кроссовок"""
    pass


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    """Админ панель Брендов"""
    pass


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Админ панель Категорий"""
    pass
