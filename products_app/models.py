from django.db import models

# Create your models here.
class Category(models.Model):

    name = models.CharField(max_length=100)

    def __str__(self):

        return self.name


class Product(models.Model):

    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    product_name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.IntegerField()
    stock = models.IntegerField(default=0)
    image = models.ImageField(upload_to='products/', blank=True, null=True)

    def __str__(self):

        return self.product_name