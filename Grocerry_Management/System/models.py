from django.db import models
from django.utils import timezone
from django.db.models import Sum
from django.db.models.functions import TruncMonth, TruncDay
from datetime import date


class Product(models.Model):
    class Meta:
        db_table = 'product'

    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name


class Transaction(models.Model):
    customer_name = models.CharField(max_length=255)
    product_purchased = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField()
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.customer_name} - {self.product_purchased} - {self.timestamp}"


class Customer(models.Model):
    class Meta:
        db_table = 'customer'

    name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=10)
    address = models.TextField()
    last_transaction = models.DateTimeField()
    passport_photo = models.ImageField(
        upload_to='passport_photos/', null=True, blank=True)
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name


class Bill(models.Model):
    customer_name = models.CharField(max_length=255)
    customer_email = models.EmailField()
    address = models.CharField(max_length=200)
    phone_number = models.CharField(max_length=10)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.customer_name}'s Bill - {self.timestamp}"
