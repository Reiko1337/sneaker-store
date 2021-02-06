from django.contrib import admin
from .models import Sneaker, Brand, Category, Size, SneakerInCart, Cart
from django.utils.html import mark_safe


class SizePanel(admin.TabularInline):
    model = Size
    extra = 1
    ordering = ['size']


class SneakerInCartPanel(admin.TabularInline):
    model = SneakerInCart
    extra = 0
    ordering = ['size__size']
    readonly_fields = ('final_price',)


@admin.register(Sneaker)
class SneakerAdmin(admin.ModelAdmin):
    """Админ панель Кроссовок"""
    list_display = ('id', 'name', 'get_brand__name', 'get_category__name', 'price', 'get_img')
    inlines = [SizePanel]
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name', 'brand__name', 'category__name')
    list_filter = ('brand__name', 'category__name')

    def get_brand__name(self, rec):
        return rec.brand.name

    get_brand__name.short_description = 'Бренд'

    def get_category__name(self, rec):
        return rec.category.name

    get_category__name.short_description = 'Категория'

    def get_img(self, rec):
        return mark_safe(f'<img src = {rec.image.url} width="100"')

    get_img.short_description = 'Фото'


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    """Админ панель Брендов"""
    search_fields = ('name',)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Админ панель Категорий"""
    search_fields = ('name',)


@admin.register(Size)
class SizeAdmin(admin.ModelAdmin):
    """Админ панель Размеров Кроссовок"""
    list_display = ('get_sneaker__name', 'size', 'quantity')
    list_editable = ('quantity',)
    search_fields = ('sneaker__name', 'size')

    def get_sneaker__name(self, rec):
        return rec.sneaker.name

    get_sneaker__name.short_description = 'Кроссовки'


@admin.register(SneakerInCart)
class SneakerInCartAdmin(admin.ModelAdmin):
    """Админ панель Кроссовок в корзине"""
    list_display = ('get_sneaker__name', 'get_size', 'get_cart__id__customer', 'quantity', 'final_price')
    readonly_fields = ('final_price',)
    search_fields = ('cart__customer__username', 'sneaker__name')

    def get_sneaker__name(self, rec):
        return rec.sneaker.name

    get_sneaker__name.short_description = 'Кроссовки'

    def get_size(self, rec):
        return rec.size.size

    get_size.short_description = 'Размер'

    def get_cart__id__customer(self, rec):
        return '{0} {1}'.format(rec.cart.id, rec.cart.customer.username)

    get_cart__id__customer.short_description = 'ID Корзина и Имя пользователя'


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    """Админ панель Корзины"""
    list_display = ('id', 'get_customer', 'total_sneaker', 'final_price', 'in_order')
    list_editable = ('in_order',)
    inlines = [SneakerInCartPanel]
    readonly_fields = ('total_sneaker', 'final_price')
    search_fields = ('customer__username',)

    def get_customer(self, rec):
        return rec.customer.username

    get_customer.short_description = 'Имя пользователя'


admin.site.site_title = 'Магазин Кроссовк'
admin.site.site_header = 'Магазин Кроссовк'
