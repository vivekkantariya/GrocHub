from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models
from django.contrib.auth.models import AbstractUser
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

    def __str__(self):
        return self.cust_name
    
class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)  # Optional field
    price = models.DecimalField(max_digits=10, decimal_places=2)
    MEASUREMENT_CHOICES = [
        ('250g', '250 Gram'),
        ('500g', '500 Gram'),
        ('1kg', '1 KG'),
        ('5kg', '5 KG'),
        ('custom', 'Custom'),
    ]
    measurement_unit = models.CharField(
        max_length=10,
        choices=MEASUREMENT_CHOICES,
        default='1kg'
    )
    custom_measurement = models.CharField(max_length=50, null=True, blank=True)
    stock = models.PositiveIntegerField(default=0)  # Stock quantity

    def __str__(self):
        return f"{self.name} - {self.measurement_unit or self.custom_measurement} ({self.stock} in stock)"
    
class Bill(models.Model):
    customer = models.ForeignKey(Customer, related_name='bills', on_delete=models.SET_NULL, null=True)
    date = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Bill #{self.id} for {self.customer}"
    
    # models.py (add to Bill model)
    def get_items(self):
        return self.transactions.all()


class Transaction(models.Model):
    bill = models.ForeignKey(Bill, on_delete=models.CASCADE, related_name='transactions')  # Added related_name here
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True) 

    def __str__(self):
        return f"{self.product.name} - {self.quantity} x {self.amount}"


    # models.py (add to Transaction model)
    def get_total(self):
        return self.quantity * self.product.price
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email is required")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_admin", True)
        extra_fields.setdefault("is_superuser", True)

        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)

    # Required fields for Django's authentication system
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []  # No extra fields required

    def __str__(self):
        return self.email

    @property
    def is_staff(self):
        return self.is_admin
