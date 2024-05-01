from django.urls import path
from .views import *

urlpatterns = [
    path('', CartRetrieveView.as_view(), name='cart-retrieve'),
    path('items/', CartItemListCreateView.as_view(), name='cart-item-create'),
]

