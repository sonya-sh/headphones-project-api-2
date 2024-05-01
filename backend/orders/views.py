from django.shortcuts import render, get_object_or_404
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTStatelessUserAuthentication
from .serializers import OrderSerializer, OrderDetailSerializer
from .models import Order, OrderItem
from cart.models import Cart



class OrderListCreateView(generics.ListCreateAPIView):

    authentication_classes = [JWTStatelessUserAuthentication]
    permission_classes = [IsAuthenticated]

    serializer_class = OrderSerializer

    def get_queryset(self):
        user_id = self.request.user.id
        queryset = Order.objects.filter(user_id_field=user_id) 
        return queryset
    

    def post(self, request, *args, **kwargs):
        user_id = request.user.id 
        
        cart = get_object_or_404(Cart, user_id=user_id)
        cart_items = cart.items.filter(selected_for_order=True)
        
        if not cart_items.exists():
            return Response({"error": "Корзина пуста или ничего не отмечено для заказа"}, status=status.HTTP_400_BAD_REQUEST)
    
        order = Order.objects.create(user_id_field=user_id, total_amount=0)

        total_price = 0
        for cart_item in cart_items:
            order_item = OrderItem.objects.create(order=order, product=cart_item.product, quantity=cart_item.quantity)
            total_price += cart_item.total_price()
        
        order.total_amount = total_price
        #order.items.set(cart_items)
        order.save()

        cart.products.clear()
        
        serializer = OrderSerializer(order)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    

class OrderDetailApiView(generics.RetrieveAPIView):

    authentication_classes = [JWTStatelessUserAuthentication]
    permission_classes = [IsAuthenticated]

    serializer_class = OrderDetailSerializer
    queryset = Order.objects.all()

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()  # Получаем конкретный заказ
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
