from django.shortcuts import render, redirect
from .forms import ProductForm
from .models import Product

# Create your views here.
def homeView(request, undefined_path=None):
    return render(request, "home.html")

def loginView(request):
    return render(request, "loginpage.html")

def manageProductView(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('manage_product')
    else:
        form = ProductForm()

    return render(request, 'productpage.html', {'form': form})

def customerPageView(request):
    return render(request, "home.html", {'section': 'customer_page'})

def transactionView(request):
    return render(request, 'transaction.html')

def AnalysisView(request):
    return render(request, 'analysis.html')

def customersView(request):
    return render(request, 'customers.html')

def BillingView(request):
    return render(request, 'billing.html')

def addproductView(request):
    products = Product.objects.all()
    return render(request, 'productpage.html', {'products': products})