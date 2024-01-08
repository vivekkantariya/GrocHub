from django.urls import path, reverse_lazy
from django.shortcuts import render, redirect
from .forms import ProductForm
from .models import Product

# Create your views here.
def homeView(request, undefined_path=None):
    return render(request, "home.html")

def loginView(request):
    return render(request, "loginpage.html")

def manageProductView(request):
    return render(request, "home.html", {'section': 'manage_product'})

def customerPageView(request):
    return render(request, "home.html", {'section': 'customer_page'})

def transactionView(request):
    return render(request, 'transaction.html')

def AnalysisView(request):
    return render(request, 'analysis.html')

def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            # Save the form data to the database
            product_instance = Product(
                product_name=form.cleaned_data['product_name'],
                category=form.cleaned_data['category'],
                price=form.cleaned_data['price']
            )
            product_instance.save()

            return redirect('productpage.html')  # Redirect to a success page
    else:
        form = ProductForm()

    return render(request, 'productpage.html', {'form': form})