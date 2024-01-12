from django.shortcuts import render, redirect
from .forms import CustomerForm, ProductForm, BillForm
from .models import Product, Customer
from django.core.mail import send_mail
from django.shortcuts import render
from .forms import BillForm
from .models import Product
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
            return redirect('productl   ist')  # Redirect to the correct URL
        else:
            return render(request, 'addproduct.html', {'form': form})
    else:
        form = ProductForm()
        return render(request, 'addproduct.html', {'form': form})
        
def transactionView(request):
    return render(request, 'transaction.html')

def AnalysisView(request):
    return render(request, 'analysis.html')

def send_email(to_email, subject, message):
    send_mail(subject, message, 'grochub1@yahoo.com', [to_email], fail_silently=False)

def bill_view(request):
    if request.method == 'POST':
        form = BillForm(request.POST)
        if form.is_valid():
            # Process the form data, generate the bill, and send email
            customer_email = form.cleaned_data['customer_email']
            products = form.cleaned_data['products']

            # Example: Generate the bill content
            bill_content = f"Thank you for your purchase!\n\nProducts: {', '.join([product.name for product in products])}\nTotal: ${sum([product.price for product in products]):.2f}"

            # Send the email
            send_email(customer_email, 'Your Grocery Bill', bill_content)

            return render(request, 'success.html')
    else:
        form = BillForm()

    return render(request, 'billing.html', {'form': form})
    
def get_product_suggestions(request):
    search_term = request.GET.get('search', '')

    # Fetch product suggestions from the database
    products = Product.objects.filter(name__icontains=search_term)[:5]

    # Return a JSON response with product details (including price)
    suggestions = [{'name': product.name, 'price': float(product.price)} for product in products]
    
    return JsonResponse(suggestions, safe=False)
