from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Cart, CartItem
from .serializers import CartSerializer, CartItemSerializer

    
class CartRetrieveView(generics.RetrieveAPIView):
    
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self): 

        try:
            obj = Cart.objects.get(user_id=self.request.user.id)
        except Cart.DoesNotExist:
            obj = Cart.objects.create(user_id=self.request.user.id)

        self.check_object_permissions(self.request, obj)

        return obj
        
    
class CartItemListCreateView(generics.ListCreateAPIView):

    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        cart = self.get_or_create_cart(request.user.id)
        product = serializer.validated_data['product']
        quantity = serializer.validated_data.get('quantity', 1)

        cart_item = CartItem.objects.filter(cart=cart, product=product).first()
        if cart_item:
            self.update_cart_item_quantity(cart_item, quantity)
            return Response(self.get_serializer(cart_item).data, status=status.HTTP_200_OK)
        else:
            self.create_cart_item(serializer, cart)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def get_or_create_cart(self, user_id):
        cart, created = Cart.objects.get_or_create(user_id=user_id)
        return cart

    def update_cart_item_quantity(self, cart_item, quantity):
        cart_item.quantity += quantity
        cart_item.save()

    def create_cart_item(self, serializer, cart):
        serializer.save(cart=cart)

