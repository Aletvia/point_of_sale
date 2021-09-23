
from django.urls import path
from .views import *


urlpatterns = [
    path(
        '',
        ProductsView.as_view(),
        name='products'
    ),
    path(
        '<str:id>/',
        ProductsView.as_view(),
        name='products'
    )
]