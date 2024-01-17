from django.core.mail import EmailMessage
from django.shortcuts import render, redirect
from .forms import CustomerForm, ProductForm, BillForm
from .models import Product, Customer
from django.core.mail import send_mail, EmailMessage
from django.shortcuts import render
from .forms import BillForm
from .models import Product, Transaction
from django.http import JsonResponse
from django.utils import timezone
from datetime import timedelta
from django.db.models import Sum
from django.db.models import F, ExpressionWrapper, DecimalField
from django.db.models.functions import TruncMonth
from django.db.models import Count
import json

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
    # Get transactions from the last 24 hours
    start_time = timezone.now() - timedelta(days=1)
    transactions = Transaction.objects.filter(timestamp__gte=start_time)

    return render(request, 'transaction.html', {'transactions': transactions})

def AnalysisView(request):
    return render(request, 'analysis.html')


def send_email(to_email, subject, message):
    send_mail(subject, message, 'grochub1@yahoo.com',
              [to_email], fail_silently=False)


def bill_view(request):
    return render(request, 'billing.html')


def get_product_suggestions(request):
    search_term = request.GET.get('search', '')

    # Fetch product suggestions from the database
    products = Product.objects.filter(name__icontains=search_term)[:5]

    # Return a JSON response with product details (including price)
    suggestions = [{'name': product.name, 'price': float(
        product.price)} for product in products]

    return JsonResponse(suggestions, safe=False)


def generate_bill(request):
    if request.method == 'POST':
        form = BillForm(request.POST)
        if form.is_valid():
            customer_email = form.cleaned_data['customer_email']
            # Get list of selected products
            products = request.POST.getlist('products')
            # Get list of corresponding quantities
            quantities = request.POST.getlist('quantity')

            # Validate product names and retrieve product details
            valid_products = []
            total_price = 0
            for product_name, quantity in zip(products, quantities):
                product = Product.objects.filter(
                    name__iexact=product_name).first()
                if product:
                    valid_products.append({'name': product.name, 'quantity': int(
                        quantity), 'price': float(product.price)})
                    total_price += float(product.price) * int(quantity)
                else:
                    return JsonResponse({'success': False, 'errors': [f'"{product_name}" is not a valid value.']})

            # Additional logic for storing the transaction can be added here

            # Send email with the bill details
            email_subject = 'Your Bill Details'
            email_message = f'Thank you for your purchase!\n\n'
            email_message += 'Products:\n'
            for product in valid_products:
                email_message += f'{product["name"]} - Quantity: {product["quantity"]} - Price: ${product["price"]}\n'
            email_message += f'\nTotal Price: ${total_price}'

            send_email_with_attachment(
                customer_email, email_subject, email_message)

            # Return a JSON response with success and customer email
            return JsonResponse({'success': True, 'customer_email': customer_email})
        else:
            return JsonResponse({'success': False, 'errors': form.errors})
    else:
        return JsonResponse({'success': False, 'errors': 'Invalid request method'})


def send_email_with_attachment(to_email, subject, message):
    try:
        email = EmailMessage(subject, message, 'grochub1@yahoo.com', [to_email])
        email.send(fail_silently=False)
        print("Email sent successfully")
        return JsonResponse({'success': True, 'message': 'Email sent successfully'})
    except Exception as e:
        error_message = str(e)
        print(f"Error sending email: {error_message}")
        return JsonResponse({'success': False, 'error': error_message})
    

def get_monthly_income(request):
    monthly_income_data = Transaction.objects.annotate(
        month=TruncMonth('timestamp')
    ).values('month').annotate(
        total_income=ExpressionWrapper(
            Sum(F('quantity') * F('product_purchased')),
            output_field=DecimalField(),
        )
    ).order_by('month')

    labels = [item['month'].strftime('%B %Y') for item in monthly_income_data]
    data = [item['total_income'] for item in monthly_income_data]

    return JsonResponse({'labels': labels, 'data': data})

def get_real_time_customers(request):
    # Get real-time customer data for the last 24 hours
    start_time = timezone.now() - timedelta(days=1)
    real_time_customer_data = Transaction.objects.filter(timestamp__gte=start_time).values('timestamp').annotate(customer_count=Count('id')).order_by('timestamp')
    
    labels = [item['timestamp'].strftime('%H:%M') for item in real_time_customer_data]
    data = [item['customer_count'] for item in real_time_customer_data]

    return JsonResponse({'labels': labels, 'data': data})