from django.db import models

class Product(models.Model):
    UNIT_CHOICES = [
        ('each', 'Each'),
        ('kg', 'Kilogram'),
    ]
    name = models.CharField(max_length=100)
    price = models.FloatField()
    quantity = models.FloatField(default=0)  # Available stock
    unit = models.CharField(max_length=10, choices=UNIT_CHOICES)

    def __str__(self):
        return self.name


class Order(models.Model):
    customer_name = models.CharField(max_length=100)
    total_price = models.FloatField()
    products = models.TextField()  # Store product details as a text list or JSON string

    def __str__(self):
        return f"Order by {self.customer_name}"
