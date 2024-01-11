from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)

class Transaction(models.Model):
    customer_name = models.CharField(max_length=255)
    product_purchased = models.CharField(max_length=255)
    quantity = models.IntegerField()

class Customer(models.Model):
    class Meta:
        db_table = 'customer'
    
    name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=10)
    address = models.TextField()
    last_transaction = models.DateTimeField()
    passport_photo = models.ImageField(upload_to='passport_photos/', null=True, blank=True)

    def __str__(self):
        return self.name

    