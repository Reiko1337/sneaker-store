from django.urls import path
from . import views


app_name = 'store'

urlpatterns = [
    path('', views.Index.as_view(), name='index'),
    path('cart/<str:sneaker_id>/<str:size>/delete/', views.DeleteSneakerCart.as_view(), name='delete_sneaker_from_cart'),
    path('sneaker/<slug:sneaker>/add-to-cart/', views.AddToCart.as_view(), name='add_to_cart'),
    path('sneaker/<slug:sneaker>/add-to-favorites/', views.EditFavorites.as_view(), name='edit_favorites'),
    path('sneaker/<str:brand>/<slug:sneaker>/', views.DetailSneaker.as_view(), name='detail'),

]
