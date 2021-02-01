from django.contrib import admin
from .models import Sneaker, Brand, Category


@admin.register(Sneaker)
class SneakerAdmin(admin.ModelAdmin):
    pass


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    pass


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass
