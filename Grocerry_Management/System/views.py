from django.shortcuts import render, redirect
from .forms import CustomerForm, ProductForm
from .models import Product, Customer
from django.http import JsonResponse


# Create your views here.
def homeView(request, undefined_path=None):
    return render(request, "home.html")

def loginView(request):
    return render(request, "loginpage.html")

def manageProductView(request):
    products = Product.objects.all()

    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('manage_product')
    else:
        form = ProductForm()

    return render(request, 'productpage.html', {'form': form, 'products': products})

def customer_list(request):
    customers = Customer.objects.all()
    return render(request, 'customers.html', {'customer': customers})

def transactionView(request):
    return render(request, 'transaction.html')

def AnalysisView(request):
    return render(request, 'analysis.html')

def BillingView(request):
    return render(request, 'billing.html')

def addproductView(request):
    products = Product.objects.all()
    return render(request, 'productpage.html', {'products': products})

def add_product(request):
    if request.method == 'POST':
        name = request.POST.get('manageProductName')
        price = request.POST.get('manageProductPrice')
        product = Product.objects.create(name=name, price=price)

        return JsonResponse({'id': product.id, 'name': product.name, 'price': product.price})
    else:
        return JsonResponse({'error': 'Invalid request method'})


# def customerPageView(request):
#     if request.method == 'POST':
#         form = CustomerForm(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#             # Add any additional logic or redirect as needed
#     else:
#         form = CustomerForm()

#     customers = Customer.objects.all()
#     return render(request, "customers.html", {'section': 'customer_page', 'customers': customers, 'form': form})
