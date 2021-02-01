# Generated by Django 3.1.5 on 2021-01-31 23:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Brand',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=120, verbose_name='Бренд')),
            ],
            options={
                'verbose_name': 'Бренд',
                'verbose_name_plural': 'Бренды',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=120, verbose_name='Категория')),
            ],
            options={
                'verbose_name': 'Категория',
                'verbose_name_plural': 'Категории',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='Sneaker',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=120, verbose_name='Название')),
                ('image', models.ImageField(upload_to='', verbose_name='Фотография')),
                ('sex', models.CharField(choices=[(None, 'Выберите пол'), ('male', 'Мужские'), ('woman', 'Женские')], db_index=True, max_length=20, verbose_name='Пол')),
                ('feature', models.CharField(max_length=255, verbose_name='Особенность')),
                ('description', models.TextField(verbose_name='Описание')),
                ('material', models.CharField(max_length=150, verbose_name='Материал')),
                ('colour', models.CharField(max_length=120, verbose_name='Цвет')),
                ('country_manufacture', models.CharField(max_length=100, verbose_name='Страна производства')),
                ('article_number', models.CharField(max_length=60, unique=True, verbose_name='Артикул')),
                ('slug', models.SlugField(unique=True, verbose_name='URL')),
                ('brand', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='store.brand', verbose_name='Бренд')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='store.category', verbose_name='Категория')),
            ],
            options={
                'verbose_name': 'Кроссовок',
                'verbose_name_plural': 'Кроссовоки',
                'ordering': ['-id'],
            },
        ),
    ]