# Generated by Django 3.1.5 on 2021-02-05 17:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0011_auto_20210205_1943'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sneakerincart',
            name='cart',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.cart', verbose_name='Корзина'),
        ),
    ]
