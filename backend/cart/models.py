from django.db import models
from products.models import Product

class Cart(models.Model):
    user_id = models.IntegerField()
    products = models.ManyToManyField(Product, through='CartItem')

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    selected_for_order = models.BooleanField(default=True)

    def total_price(self):
        return self.product.price * self.quantity
    