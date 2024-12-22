from django.db import models
from django.utils import timezone


class Product(models.Model):
    class Meta:
        db_table = 'product'

    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name
    
class Customer(models.Model):
    cust_id = models.AutoField(primary_key=True)
    cust_name = models.CharField(max_length=255)
    cust_email = models.EmailField(unique=True)
    phone_no = models.CharField(max_length=15, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    DOB = models.DateField(null=True, blank=True)
    passport_photo = models.ImageField(upload_to='passport_photos/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)  # auto_now_add for current timestamp behavior

    class Meta:
        db_table = 'customer'

    def __str__(self):
        return self.cust_name

class Bill(models.Model):
    class Meta:
        db_table = 'system_bill'

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)  # Foreign key reference to Customer
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Bill ID: {self.id} - {self.customer.cust_name}"  # Change 'name' to 'cust_name'


class Transaction(models.Model):
    class Meta:
        db_table = 'system_transaction'

    bill = models.ForeignKey(Bill, on_delete=models.CASCADE)  # Foreign key reference to Bill
    product = models.ForeignKey(Product, on_delete=models.CASCADE)  # Foreign key reference to Product
    quantity = models.IntegerField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)  # Matches DB schema
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Transaction ID: {self.id} - {self.product.name} x {self.quantity}"
