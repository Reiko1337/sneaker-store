from django.contrib import admin
from .models import Sneaker, Brand, Category, Size


class SizePanel(admin.TabularInline):
    model = Size
    extra = 1
    ordering = ['size']


@admin.register(Sneaker)
class SneakerAdmin(admin.ModelAdmin):
    """Админ панель Кроссовок"""
    inlines = [SizePanel]


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    """Админ панель Брендов"""
    pass


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Админ панель Категорий"""
    pass


@admin.register(Size)
class CategoryAdmin(admin.ModelAdmin):
    """Админ панель Размеров Кроссовок"""
    pass
