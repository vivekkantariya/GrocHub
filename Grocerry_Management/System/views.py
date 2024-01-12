from django.shortcuts import render, redirect
from .forms import CustomerForm, ProductForm
from .models import Product, Customer
from django.http import JsonResponse


# Create your views here.
def homeView(request, undefined_path=None):
    return render(request, "home.html")

def loginView(request):
    return render(request, "loginpage.html")

def product_list(request):
    products = Product.objects.all()
    return render(request, 'products.html', {'product': products})
    
def customer_list(request):
    customers = Customer.objects.all()
    return render(request, 'customers.html', {'customer': customers})

def addproductView(request):
    return render(request, 'addproduct.html')

def addcustomerView(request):
    return render(request, 'addcustomer.html')

def add_customerView(request):
    if request.method == 'POST':
        form = CustomerForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('customerslist')
        else:
            return render(request, 'addcustomer.html', {'form': form})
    else:
        form = CustomerForm()
        return render(request, 'addcustomer.html', {'form': form})

    
def add_productView(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('productlist')  # Redirect to the correct URL
        else:
            return render(request, 'addproduct.html', {'form': form})
    else:
        form = ProductForm()
        return render(request, 'addproduct.html', {'form': form})
        
def transactionView(request):
    return render(request, 'transaction.html')

def AnalysisView(request):
    return render(request, 'analysis.html')

def BillingView(request):
    return render(request, 'billing.html')

    