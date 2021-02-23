from django.shortcuts import render, redirect, reverse, HttpResponse
from django.http import JsonResponse
from django.views.generic import ListView, DetailView, View
from .models import Sneaker, Size, SneakerInCart
from .services import get_sneaker_by_slug, get_size_sneaker, add_to_cart, get_sneaker_new, get_sneaker_sale, \
    add_sneaker_view_in_cookie, get_sneakers_view_from_cookie, edit_favorites_sneakers, get_favorites_sneakers
from .mixins import CartMixin, SessionMixin
from django.contrib import messages


class Index(ListView):
    """Главная страница"""

    template_name = 'store/index.html'
    context_object_name = 'sneakers'

    def get_queryset(self):
        return get_sneaker_new()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sneakers_sale'] = get_sneaker_sale()
        context['sneakers_view'] = get_sneakers_view_from_cookie(self.request)
        context['favorites'] = get_favorites_sneakers(self.request)

        return context


class DetailSneaker(DetailView):
    """Страница Кроссовок"""

    model = Sneaker
    template_name = 'store/detail.html'
    slug_url_kwarg = 'sneaker'

    def render_to_response(self, context, **response_kwargs):
        response = super().render_to_response(context, **response_kwargs)
        response = add_sneaker_view_in_cookie(self.request, response, context.get('sneaker'))
        return response

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


class EditFavorites(SessionMixin, View):
    """Редоктирование список избранных кроссовок"""
    def get(self, request, sneaker):
        if request.is_ajax():
            status = edit_favorites_sneakers(request,  sneaker)
            if status:
                return JsonResponse({'success': True}, status=200)
            else:
                return JsonResponse({'success': False}, status=404)

        return redirect('store:index')
