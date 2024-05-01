from rest_framework.serializers import ModelSerializer
from .models import Order, OrderItem

class OrderItemSerializer(ModelSerializer):

    class Meta:
        model = OrderItem
        fields = ['product', 'quantity']

class OrderDetailSerializer(ModelSerializer):

    items = OrderItemSerializer(many=True)
    class Meta:
        model = Order
        fields = ['id', 'user_id_field', 'items', 'total_amount']

class OrderSerializer(ModelSerializer):

    class Meta:
        model = Order
        fields = ['id', 'user_id_field', 'total_amount']


