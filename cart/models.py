from django.db import models
from django.contrib.auth.models import User
from product.models import Product

class Cart(models.Model):
    #each cart belongs to a user
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    #set timestamp once when a cart is first created
    created_at = models.DateTimeField(auto_now_add=True)
    #set timestamp every time the cart is updated
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    @property
    def total(self):
        #sum of subtotal of each item in the cart
        return sum(item.subtotal for item in self.items.all())

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price_at_addition = models.DecimalField(max_digits=10,decimal_places=2)

    @property
    def subtotal(self):
        return self.quantity * self.price_at_addition
