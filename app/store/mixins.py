from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from .models import Cart

from .session import Session


class CartMixin:
    def setup(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            user = get_object_or_404(User, username=request.user.username)
            self.cart, create = Cart.objects.get_or_create(customer=user)
        return super().setup(request, *args, **kwargs)


class SessionMixin:
    def setup(self, request, *args, **kwargs):
        self.session = Session(request)
        return super().setup(request, *args, **kwargs)
