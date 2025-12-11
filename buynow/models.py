from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.FloatField()
    quantity = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name


class Sale(models.Model):
    PAYMENT_CHOICES = [
        ('Bank', 'Bank Transfer'),
        ('eSewa', 'eSewa'),
        ('Khalti', 'Khalti'),
    ]

    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    total_price = models.FloatField()
    payment_method = models.CharField(max_length=20, choices=PAYMENT_CHOICES)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.product.name} - {self.payment_method} ({self.date.date()})"
