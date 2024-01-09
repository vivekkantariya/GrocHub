from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name

class Transaction(models.Model):
    customer_name = models.CharField(max_length=255)
    product_purchased = models.CharField(max_length=255)
    quantity = models.IntegerField()

class CustomerProfile(models.Model):
    name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20)
    address = models.TextField()
    last_transaction = models.DateTimeField()

    def __str__(self):
        return self.name
    