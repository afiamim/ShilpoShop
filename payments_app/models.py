from django.db import models

# Create your models here.
from django.db import models

from orders_app.models import Order


class Payment(models.Model):

    METHOD_CHOICES = [

        ('Cash', 'Cash'),

        ('Card', 'Card'),

        ('Bkash', 'Bkash'),

    ]

    STATUS_CHOICES = [

        ('Pending', 'Pending'),

        ('Completed', 'Completed'),

    ]

    order = models.OneToOneField(
        Order,
        on_delete=models.CASCADE
    )

    payment_method = models.CharField(
        max_length=20,
        choices=METHOD_CHOICES
    )

    amount = models.IntegerField()

    payment_status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='Pending'
    )

    def __str__(self):

        return self.payment_method