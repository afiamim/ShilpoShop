from django.db import models

# Create your models here.
from django.db import models

from django.contrib.auth.models import User

from products_app.models import Product


class Review(models.Model):

    RATING_CHOICES = [

        (1, '1 Star'),

        (2, '2 Star'),

        (3, '3 Star'),

        (4, '4 Star'),

        (5, '5 Star'),

    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE
    )

    rating = models.IntegerField(
        choices=RATING_CHOICES
    )

    comment = models.TextField()

    def __str__(self):

        return self.user.username