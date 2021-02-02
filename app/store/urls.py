from django.urls import path
from . import views


app_name = 'store'

urlpatterns = [
    path('', views.Index.as_view(), name='index'),
    path('sneaker/<str:brand>/<slug:sneaker>', views.DetailSneaker.as_view(), name='detail')
]
