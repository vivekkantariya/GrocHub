from django.db import models

class Customer(models.Model):
    REGULAR = 'R'
    NON_REGULAR = 'NR'
    
    CUSTOMER_TYPES = [
        (REGULAR, 'Regular'),
        (NON_REGULAR, 'Non-Regular'),
    ]

    cust_name = models.CharField(max_length=100)
    cust_email = models.EmailField(unique=True)
    phone_no = models.CharField(max_length=15)
    address = models.CharField(max_length=255, null=True, blank=True)
    customer_type = models.CharField(
        max_length=2,
        choices=CUSTOMER_TYPES,
        default=REGULAR
    )
    dob = models.DateField(null=True, blank=True)  # Added Date of Birth field
    passport_photo = models.ImageField(upload_to='passport_photos/', null=True, blank=True)
    dob = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.cust_name

class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name

class Bill(models.Model):
    customer = models.ForeignKey(Customer, related_name='bills', on_delete=models.SET_NULL, null=True)
    date = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    def __str__(self):
        return f"Bill #{self.id} for {self.customer}"
    
class Transaction(models.Model):
    bill = models.ForeignKey(Bill, on_delete=models.CASCADE, related_name='transactions')  # Added related_name here
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True) 
    
    def __str__(self):
        return f"{self.product.name} - {self.quantity} x {self.amount}"

