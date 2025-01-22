from django import forms
from .models import Product, Customer, Bill, Transaction

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'price', 'measurement_unit', 'custom_measurement']

    def clean(self):
        cleaned_data = super().clean()
        measurement_unit = cleaned_data.get('measurement_unit')
        custom_measurement = cleaned_data.get('custom_measurement')

        if measurement_unit == 'custom' and not custom_measurement:
            raise forms.ValidationError('Custom measurement must be provided if "Custom" is selected.')

        return cleaned_data

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['bill', 'product', 'quantity']  # Changed to match the new model fields

    def clean_quantity(self):
        quantity = self.cleaned_data['quantity']
        if quantity <= 0:
            raise forms.ValidationError('Quantity must be greater than zero.')
        return quantity
    
class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['cust_name', 'cust_email', 'phone_no', 'address', 'dob', 'passport_photo']  # Include passport_photo

    def clean_phone_no(self):
        phone_no = self.cleaned_data['phone_no']
        if not phone_no.isdigit():
            raise forms.ValidationError('Phone number must contain only digits.')
        return phone_no

    def clean_cust_email(self):
        cust_email = self.cleaned_data['cust_email']
        if Customer.objects.filter(cust_email=cust_email).exists():
            raise forms.ValidationError('Email is already registered.')
        return cust_email

    def clean_passport_photo(self):
        passport_photo = self.cleaned_data.get('passport_photo')
        if passport_photo and not passport_photo.name.lower().endswith(('jpg', 'jpeg', 'png')):
            raise forms.ValidationError('File must be a JPG, JPEG, or PNG image.')
        return passport_photo


class BillForm(forms.ModelForm):
    class Meta:
        model = Bill
        fields = ['customer', 'total']  # Updated to reflect the foreign key relationship

    def clean_total(self):
        total = self.cleaned_data['total']
        if total <= 0:
            raise forms.ValidationError('Total amount must be greater than zero.')
        return total
