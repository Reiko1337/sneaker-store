from django.shortcuts import render, redirect, reverse
from django.views.generic import ListView, DetailView, View
from .models import Sneaker, Size, SneakerInCart

from .services import get_sneaker_by_slug, get_size_sneaker, add_to_cart, get_sneaker_new, get_sneaker_sale
from .mixins import CartMixin


class Index(ListView):
    """Главная страница"""

    template_name = 'store/index.html'
    context_object_name = 'sneakers'

    def get_queryset(self):
        return get_sneaker_new()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sneakers_sale'] = get_sneaker_sale()
        return context


class DetailSneaker(DetailView):
    """Страница Кроссовок"""

    model = Sneaker
    template_name = 'store/detail.html'
    slug_url_kwarg = 'sneaker'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        sneaker = super().get_object()
        context['sizes'] = get_size_sneaker(sneaker)
        return context


class AddToCart(CartMixin, View):
    """Добавление а корзину"""

    def post(self, request, sneaker):
        sneaker = get_sneaker_by_slug(sneaker)
        sizes = get_size_sneaker(sneaker)
        add_to_cart(request, sizes, sneaker, self.cart)
        return redirect('store:detail', brand=sneaker.brand.name, sneaker=sneaker.slug)
