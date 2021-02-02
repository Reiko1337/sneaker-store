from django.db import models
from django.core.validators import MinValueValidator
from django.urls import reverse


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
