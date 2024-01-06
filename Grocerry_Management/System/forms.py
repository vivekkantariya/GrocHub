from django import forms

class ProductForm(forms.Form):
    product_name = forms.CharField(label='Product Name', max_length=100)
    category = forms.CharField(label='Category', max_length=100)
    price = forms.DecimalField(label='Price', min_value=0, decimal_places=2)

class TransactionForm(forms.Form):
    customer_name = forms.CharField(label='Customer Name', max_length=255)
    product_purchased = forms.CharField(label='Product Purchased', max_length=255)
    quantity = forms.IntegerField(label='Quantity')

class CustomerProfileForm(forms.Form):
    name = forms.CharField(label='Name', max_length=255)
    phone_number = forms.CharField(label='Phone Number', max_length=20)
    address = forms.CharField(label='Address', widget=forms.Textarea)
    last_transaction = forms.DateTimeField(label='Last Transaction')