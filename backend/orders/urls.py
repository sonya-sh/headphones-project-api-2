from django.urls import path
from .views import *

urlpatterns = [
    path('orders/', OrderListCreateView.as_view()),
    path('order_detail/<int:pk>/', OrderDetailApiView.as_view()),
]
