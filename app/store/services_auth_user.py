from .models import SneakerInCart, Cart
from django.contrib import messages


def get_cart_auth_user(request: object):
    """Получить корзину пользователя"""
    if request.user.is_authenticated:
        user = request.user
        cart, create = Cart.objects.get_or_create(customer=user)
    return cart


class CartUser:
    def __init__(self, request):
        self.request = request
        self.cart = get_cart_auth_user(self.request)

    def add_to_cart(self, sneaker, size):
        sneaker_in_cart, create = SneakerInCart.objects.get_or_create(cart=self.cart, sneaker=sneaker, size=size)
        if not create:
            if sneaker_in_cart.quantity < size.quantity:
                sneaker_in_cart.quantity += 1
                sneaker_in_cart.save()
            else:
                messages.error(self.request,
                               'Кроссовок {0} | Размер ({1}) больше нет в наличии'.format(sneaker.name, size))
                return
        messages.success(self.request, 'Кроссовки {0} | Размер ({1}) добавлены в корзину'.format(sneaker.name, size))

    def get_final_price(self):
        return self.cart.final_price

    def get_total_sneaker(self):
        return self.cart.total_sneaker

    def __iter__(self):
        cart_view = {}
        for item in self.cart.sneakerincart_set.all():
            if not cart_view.get(str(item.pk)):
                cart_view[str(item.pk)] = {}
            cart_view[str(item.pk)][
                str(item.size.size).rstrip('0').rstrip('.') if '.' in str(item.size.size) else str(item.size.size)] = {
                'quantity': item.quantity,
                'final_price': item.final_price,
                'sneaker': item.sneaker,
            }
            if item.sneaker.sale:
                cart_view[str(item.pk)][
                    str(item.size.size).rstrip('0').rstrip('.') if '.' in str(item.size.size) else str(item.size.size)][
                    'discount_price'] = item.quantity * item.sneaker.discount_price
                cart_view[str(item.pk)][
                    str(item.size.size).rstrip('0').rstrip('.') if '.' in str(item.size.size) else str(item.size.size)][
                    'final_price'] = item.quantity * item.sneaker.price

        for items in cart_view.values():
            for size, item in items.items():
                item['size'] = size
                yield item

    def remove(self, sneaker, size):
        sneaker = self.cart.sneakerincart_set.filter(sneaker__pk=sneaker, size__size=size).first()
        if sneaker:
            sneaker.delete()
