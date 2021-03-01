from .services_auth_user import CartUser
from .session import CartSession


def get_cart_context(request):
    if request.user.is_authenticated:
        cart_user = CartUser(request)
        return {'cart': cart_user}
    else:
        cart = CartSession(request)
        return {'cart': cart}
