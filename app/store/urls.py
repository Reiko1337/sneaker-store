from django.urls import path
from . import views


app_name = 'store'

urlpatterns = [
    path('', views.Index.as_view(), name='index'),
    path('sneaker/<slug:sneaker>/add-to-cart', views.AddToCart.as_view(), name='add_to_cart'),
    path('sneaker/<str:brand>/<slug:sneaker>', views.DetailSneaker.as_view(), name='detail'),
]
