from django.shortcuts import get_object_or_404
from .models import Sneaker
import copy
from django.contrib import messages


class Session:
    """Сессия"""
    def __init__(self, request):
        self.request = request
        self.session = request.session

    def save(self):
        self.session.modified = True


class FavoriteSession(Session):
    """Избранные кроссоки анонимного пользователя"""
    def __init__(self, request):
        super().__init__(request)
        if not self.session.get('favorites'):
            self.session['favorites'] = []

    def add_to_favorites(self, sneaker):
        self.session['favorites'].append(sneaker.slug)
        self.save()

    def remove_from_favorites(self, sneaker):
        try:
            self.session['favorites'].remove(sneaker.slug)
            self.save()
        except ValueError:
            pass

    def get_favorites_sneakers(self):
        return list(map(lambda x: get_object_or_404(Sneaker, slug=x), self.session['favorites']))


class CartSession(Session):
    """Корзина анонимного пользователя"""
    def __init__(self, request):
        super().__init__(request)

        if not self.session.get('cart'):
            self.session['cart'] = {}
        self.cart = self.session['cart']

    def add_to_cart(self, sneaker, size, quantity=1):
        """Добавить в корзину"""
        sneaker_id = str(sneaker.pk)
        size_num = str(size.size).rstrip('0').rstrip('.') if '.' in str(size.size) else str(size.size)
        if not self.session['cart'].get(sneaker_id):
            self.session['cart'][sneaker_id] = {}

        if not self.session['cart'][sneaker_id].get(size_num):
            self.session['cart'][sneaker_id][size_num] = {
                'quantity': 0,
            }

        if self.session['cart'][sneaker_id][size_num]['quantity'] < size.quantity:
            self.session['cart'][sneaker_id][size_num]['quantity'] += quantity
            messages.success(self.request,
                             'Кроссовки {0} | Размер ({1}) добавлены в корзину'.format(sneaker.name, size_num))
        else:
            messages.error(self.request,
                           'Кроссовок {0} | Размер ({1}) больше нет в наличии'.format(sneaker.name, size_num))

        self.save()

    def __iter__(self):
        self.validation_quantity()

        cart = copy.deepcopy(self.cart)
        for sneaker_id in self.cart:
            sneaker = get_object_or_404(Sneaker, pk=sneaker_id)
            for size in cart[sneaker_id]:
                quantity = cart[sneaker_id][size]['quantity']
                if sneaker.sale:
                    cart[sneaker_id][size]['discount_price'] = str(sneaker.discount_price * quantity)

                cart[sneaker_id][size]['final_price'] = str(sneaker.price * quantity)
                cart[sneaker_id][size]['sneaker'] = sneaker

        for items in reversed(cart.values()):
            for size, item in items.items():
                item['size'] = size
                yield item

    def get_final_price(self):
        """Итоговая цена"""
        final_price = 0
        for sneaker_id in self.cart:
            sneaker = get_object_or_404(Sneaker, pk=sneaker_id)
            for size in self.cart[sneaker_id]:
                if sneaker.sale:
                    price = sneaker.discount_price
                else:
                    price = sneaker.price
                quantity = self.cart[sneaker_id][size]['quantity']
                final_price += price * quantity
        return final_price

    def get_total_sneaker(self):
        """Количество кроссовок"""
        self.validation_quantity()
        return sum(item['quantity'] for items in self.cart.values() for item in items.values())

    def validation_quantity(self):
        """Проверка количества кроссовок"""
        cart = copy.deepcopy(self.cart)
        for sneaker_id in cart:
            sneaker = get_object_or_404(Sneaker, pk=sneaker_id)
            for size in cart[sneaker_id]:
                size_sneaker = sneaker.size_set.filter(size=size).first()
                quantity = size_sneaker.quantity
                if quantity == 0:
                    self.delete_sneaker_from_cart(sneaker_id, size)
                else:
                    if self.cart[sneaker_id][size]['quantity'] > size_sneaker.quantity:
                        self.cart[sneaker_id][size]['quantity'] = size_sneaker.quantity
                        self.save()

    def delete_sneaker_from_cart(self, sneaker_id, size):
        """Удалить кроссовки из корзины"""
        sneaker_id = str(sneaker_id)
        size = str(size)
        if self.cart.get(sneaker_id):
            if self.cart[sneaker_id].get(size):
                del self.cart[sneaker_id][size]
                self.save()
                messages.success(self.request, 'Кроссовки удалены из корзины')
                return
        messages.error(self.request, 'Ошибка удаления')
