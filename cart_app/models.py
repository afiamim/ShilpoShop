from django.db import models
from django.contrib.auth.models import User
from products_app.models import Product

# Create your models here.
class CartItem(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.user.username} - {self.product.product_name}"

    @property
    def subtotal(self):
        return self.product.price * self.quantity
