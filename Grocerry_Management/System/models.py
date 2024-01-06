from django.db import models

class Product(models.Model):
    product_name = models.CharField(max_length=255)
    price = models.IntegerField()
    category = models.CharField(max_length=100)  # Add category field


    def __str__(self):
        return self.product_name

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
    