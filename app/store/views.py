from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Sneaker, Size
from django.views.generic.edit import FormMixin
from .forms import SizeFormSet


class Index(ListView):
    template_name = 'store/index.html'
    context_object_name = 'sneakers'

    def get_queryset(self):
        return Sneaker.objects.all()[:6]


class DetailSneaker(DetailView):
    model = Sneaker
    template_name = 'store/detail.html'
    slug_url_kwarg = 'sneaker'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        sneaker = super().get_object()
        context['sizes'] = sneaker.size_set.order_by('size').all()
        return context
