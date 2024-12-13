from django.db import models
from users.models import FirebaseUser
from products.models import Product

# Create your models here.
class CartItem(models.Model):
        user = models.ForeignKey(FirebaseUser, on_delete=models.CASCADE, related_name='cart_items')
        product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='cart_items')
        quantity = models.PositiveIntegerField(default=1)
        added_at = models.DateTimeField(auto_now_add=True)

        def __str__(self):
                return f"{self.product.product_name} - {self.quantity}"

        @property
        def total_price(self):
                return self.product.product_price * self.quantity
