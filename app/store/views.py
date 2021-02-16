from django.shortcuts import render, redirect, reverse
from django.views.generic import ListView, DetailView, View
from .models import Sneaker, Size, SneakerInCart

from .services import get_sneaker_by_slug, get_size_sneaker, add_to_cart
from .mixins import CartMixin


class Index(ListView):
    """Главная страница"""
    template_name = 'store/index.html'
    context_object_name = 'sneakers'

    def get_queryset(self):
        return Sneaker.objects.all()[:6]


class DetailSneaker(DetailView):
    """Страница Кроссовок"""
    model = Sneaker
    template_name = 'store/detail.html'
    slug_url_kwarg = 'sneaker'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        sneaker = super().get_object()
        context['sizes'] = sneaker.size_set.order_by('size').filter(quantity__gt=0)
        return context


class AddToCart(CartMixin, View):
    """Добавление а корзину"""

    def post(self, request, sneaker):
        sneaker = get_sneaker_by_slug(sneaker)
        sizes = get_size_sneaker(sneaker)
        add_to_cart(request, sizes, sneaker, self.cart)
        return redirect('store:detail', brand=sneaker.brand.name, sneaker=sneaker.slug)