from django import forms
from .models import Product, Customer

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'price']
        
class TransactionForm(forms.ModelForm):
    customer_name = forms.CharField(label='Customer Name', max_length=255)
    product_purchased = forms.CharField(label='Product Purchased', max_length=255)
    quantity = forms.IntegerField(label='Quantity')

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['name', 'phone_number', 'address', 'last_transaction', 'passport_photo']

class BillForm(forms.Form):
    customer_name = forms.CharField(max_length=100)
    customer_email = forms.EmailField()
    products = forms.ModelMultipleChoiceField(queryset=Product.objects.all(), widget=forms.CheckboxSelectMultiple)