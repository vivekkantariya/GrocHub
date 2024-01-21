from django import forms
from .models import Product, Customer, Bill, Transaction


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'price']


class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['customer_name', 'product_purchased', 'quantity']


class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['name', 'phone_number', 'address',
                  'last_transaction', 'passport_photo']


class BillForm(forms.ModelForm):
    class Meta:
        model = Bill
        fields = ['customer_name', 'customer_email', 'address', 'phone_number']

    def clean_phone_number(self):
        phone_number = self.cleaned_data['phone_number']
        if not phone_number.isdigit():
            raise forms.ValidationError(
                'Phone number must contain only digits.')

        return phone_number
