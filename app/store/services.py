from django.shortcuts import get_object_or_404
from .models import Sneaker, SneakerInCart
from django.contrib import messages
import ast
from .session import Session


def get_sneaker_by_slug(slug: str) -> object:
    """Крососки по URL"""
    return get_object_or_404(Sneaker, slug=slug)


def get_sneaker() -> list:
    """Все кроссовки в наличии"""
    return Sneaker.objects.filter(size__quantity__gt=0).distinct()


def get_sneaker_new() -> list:
    """Новые кроссовки (Последние 6 пар кроссок)"""
    return get_sneaker()[:6]


def get_sneaker_sale() -> list:
    """Кроссовки на скидке"""
    return get_sneaker().filter(sale=True)


def get_size_sneaker(sneaker: object) -> object:
    """Размеры кроссовок, которые в наличии"""
    return sneaker.size_set.order_by('size').filter(quantity__gt=0)


def add_sneaker_view_in_cookie(request: object, response: object, sneaker: object):
    """Добавление кроссовок в COOKIE (Которые были просмотрены пользователем)"""
    if 'sneakers' in request.COOKIES:
        sneakers = ast.literal_eval(request.COOKIES.get('sneakers'))
        if sneaker.pk not in sneakers:
            sneakers.append(sneaker.pk)
            response.set_cookie('sneakers', sneakers, max_age=1209600)
    else:
        response.set_cookie('sneakers', [sneaker.pk], max_age=1209600)
    return response


def get_sneakers_view_from_cookie(request: object):
    """Кроссовки, которые были просмотрены пользователем"""
    sneakers = []
    if request.COOKIES.get('sneakers'):
        sneakers_id = ast.literal_eval(request.COOKIES.get('sneakers'))
        for sneaker_id in sneakers_id:
            sneaker = Sneaker.objects.filter(pk=sneaker_id).first()
            if sneaker:
                sneakers.append(sneaker)
    else:
        sneakers
    return sneakers[::-1]


def get_favorites_sneakers(request: object) -> list:
    """Избранные кроссовки"""
    if request.user.is_authenticated:
        return request.user.profile.favorites_sneakers.all
    else:
        session = Session(request)
        return session.get_favorites_sneakers()


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
                    messages.error(request,
                                   'Кроссовок {0} | Размер ({1}) больше нет в наличии'.format(sneaker.name, size))
                    continue
            messages.success(request, 'Кроссовки {0} | Размер ({1}) добавлены в корзину'.format(sneaker.name, size))


def edit_favorites_sneakers(request, sneaker):
    """Редактировать список избранных кроссовок"""
    sneaker = get_sneaker_by_slug(sneaker)
    favorite = request.GET.get('favorite')
    session = Session(request)
    if favorite is not None:
        if favorite == 'true':
            request.user.profile.favorites_sneakers.add(sneaker) if request.user.is_authenticated else session.add_to_favorites(sneaker)
        elif favorite == 'false':
            request.user.profile.favorites_sneakers.remove(sneaker) if request.user.is_authenticated else session.remove_from_favorites(sneaker)
        return True
    else:
        return False

