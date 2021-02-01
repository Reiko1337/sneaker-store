from django.shortcuts import render
from django.views.generic import ListView
from .models import Sneaker


class Index(ListView):
    template_name = 'store/index.html'
    context_object_name = 'sneakers'

    def get_queryset(self):
        return Sneaker.objects.all()[:6]