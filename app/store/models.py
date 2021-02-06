from django.db import models
from django.core.validators import MinValueValidator
from django.urls import reverse
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.db.models import Sum
from django.core.exceptions import ValidationError


class Sneaker(models.Model):
    """Кроссовоки"""
    SEX = (
        (None, 'Выберите пол'),
        ('male', 'Мужские'),
        ('woman', 'Женские')
    )
    name = models.CharField(verbose_name='Название', max_length=120, db_index=True)
    image = models.ImageField(verbose_name='Фотография')
    brand = models.ForeignKey('Brand', verbose_name='Бренд', on_delete=models.PROTECT, db_index=True)
    category = models.ForeignKey('Category', verbose_name='Категория', on_delete=models.PROTECT, db_index=True)
    price = models.DecimalField(verbose_name='Цена', max_digits=9, decimal_places=2, validators=[MinValueValidator(0)])
    sex = models.CharField(verbose_name='Пол', max_length=20, choices=SEX, db_index=True)
    feature = models.CharField(verbose_name='Особенность', max_length=255)
    description = models.TextField(verbose_name='Описание')
    material = models.CharField(verbose_name='Материал', max_length=150)
    colour = models.CharField(verbose_name='Цвет', max_length=120)
    country_manufacture = models.CharField(verbose_name='Страна производства', max_length=100)
    article_number = models.CharField(verbose_name='Артикул', max_length=60, unique=True)
    slug = models.SlugField(verbose_name='URL', unique=True)

    class Meta:
        verbose_name = 'Кроссовоки'
        verbose_name_plural = 'Кроссовоки'
        ordering = ['-id']

    def get_absolute_url(self):
        return reverse('store:detail', args=[self.brand.name, self.slug])

    def __str__(self):
        return self.name


class Brand(models.Model):
    """Бренд"""
    name = models.CharField(verbose_name='Бренд', max_length=120)

    class Meta:
        verbose_name = 'Бренд'
        verbose_name_plural = 'Бренды'
        ordering = ['-id']

    def __str__(self):
        return self.name


class Category(models.Model):
    """Категория"""
    name = models.CharField(verbose_name='Категория', max_length=120)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['-id']

    def __str__(self):
        return self.name


class Size(models.Model):
    """Размер"""
    sneaker = models.ForeignKey(Sneaker, on_delete=models.CASCADE, verbose_name='Кроссовки')
    size = models.DecimalField(verbose_name='Размер', max_digits=9, decimal_places=1)
    quantity = models.PositiveIntegerField(verbose_name='Количество')

    class Meta:
        verbose_name = 'Размер'
        verbose_name_plural = 'Размеры'
        ordering = ['sneaker__name']

    def __str__(self):
        return '{0} | {1}'.format(self.sneaker.name, self.size)


class SneakerInCart(models.Model):
    sneaker = models.ForeignKey(Sneaker, verbose_name='Кроссовки', on_delete=models.PROTECT)
    size = models.ForeignKey(Size, verbose_name='Размер', on_delete=models.SET_NULL, null=True)
    cart = models.ForeignKey('Cart', verbose_name='Корзина', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(verbose_name='Количество', default=1)
    final_price = models.DecimalField(verbose_name='Общая цена', max_digits=9, decimal_places=2, default=0,
                                      validators=[MinValueValidator(0)])

    class Meta:
        verbose_name = 'Кроссовки в корзине'
        verbose_name_plural = 'Кроссовки в корзине'
        ordering = ['-id']

    def save(self, *args, **kwargs):
        self.final_price = self.quantity * self.sneaker.price
        return super().save(*args, **kwargs)

    def clean(self):
        if self.quantity > self.size.quantity:
            raise ValidationError('Нет в наличии (Доступно {0} пар кроссовок {1})'.format(self.size.quantity, self.sneaker.name))

    def __str__(self):
        return '{0} in {1}'.format(self.sneaker, self.cart.id)


class Cart(models.Model):
    customer = models.ForeignKey(User, verbose_name='Покапатель', on_delete=models.CASCADE, null=True)
    total_sneaker = models.PositiveIntegerField(verbose_name='Всего кроссовок', default=0)
    final_price = models.DecimalField(verbose_name='Общая цена', max_digits=9, decimal_places=2, default=0,
                                      validators=[MinValueValidator(0)])
    in_order = models.BooleanField(default=False, verbose_name='В заказе')

    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзины'
        ordering = ['-id']

    def __str__(self):
        return self.customer.username


@receiver(post_save, sender=SneakerInCart)
def recalculation_total_price(instance, **kwargs):
    cart = instance.cart
    cart_data = cart.sneakerincart_set.all().aggregate(Sum('final_price'), Sum('quantity'))
    if cart_data.get('final_price__sum') and cart_data.get('quantity__sum'):
        cart.final_price = cart_data['final_price__sum']
        cart.total_sneaker = cart_data['quantity__sum']
    else:
        cart.final_price = 0
        cart.total_sneaker = 0
    cart.save()
