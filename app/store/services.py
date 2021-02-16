from django.shortcuts import get_object_or_404
from .models import Sneaker, SneakerInCart
from django.contrib import messages


def get_sneaker_by_slug(slug: str) -> object:
    return get_object_or_404(Sneaker, slug=slug)


def get_size_sneaker(sneaker: object) -> object:
    return sneaker.size_set.order_by('size').filter(quantity__gt=0)


def add_to_cart(request, sizes_stock: list, sneaker: object, cart: object):
    form_sizes = set(request.POST.values())
    size = set(map(lambda size: str(size.size.normalize()), sizes_stock))

    sizes = form_sizes & size
    if not sizes:
        return messages.info(request, f'Вы не выбрали размер Кроссовок {sneaker.name}')

    for size in sizes:
        size_num = sizes_stock.filter(size=size).first()
        if size_num:
            sneaker_in_cart, create = SneakerInCart.objects.get_or_create(cart=cart, sneaker=sneaker, size=size_num)
            if not create:
                if sneaker_in_cart.quantity < size_num.quantity:
                    sneaker_in_cart.quantity += 1
                    sneaker_in_cart.save()
                else:
                    messages.error(request, 'Кроссовок {0} | Размер ({1}) больше нет в наличии'.format(sneaker.name, size))
                    continue
            messages.success(request, 'Кроссовки {0} | Размер ({1}) добавлены в корзину'.format(sneaker.name, size))