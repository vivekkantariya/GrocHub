from django.core.mail import send_mail, EmailMessage
from django.shortcuts import render, redirect, get_object_or_404
from System.utils import get_plot
from .forms import CustomerForm, ProductForm, BillForm
from .models import Product, Customer, Transaction, Bill
from django.http import JsonResponse
from django.utils import timezone
from datetime import timedelta
from django.db.models import Count, F, Sum, ExpressionWrapper
from django.db.models.functions import TruncHour, TruncMonth
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
import json
import logging
from django.template.loader import render_to_string

def homeView(request):
    return render(request, "home.html")

def loginView(request):
    return render(request, "loginpage.html")

def product_list(request):
    products = Product.objects.all()
    print(products)  # Debug statement
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
            return redirect('customer_list')
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
            return redirect('product_list')
        else:
            return render(request, 'addproduct.html', {'form': form})
    else:
        form = ProductForm()
        return render(request, 'addproduct.html', {'form': form})
def transactionView(request):
    # Get the start time for the last 24 hours
    start_time = timezone.now() - timedelta(days=1)

    # Retrieve all transactions in the last 24 hours
    transactions = Transaction.objects.filter(timestamp__gte=start_time)

    # Prepare the data to include transactions with missing customer details
    transaction_data = []
    for transaction in transactions:
        bill = transaction.bill
        if bill.customer:  # If linked to a customer in the database
            customer_name = bill.customer.cust_name
            customer_email = bill.customer.cust_email
        else:  # Handle cases where customer is missing
            customer_name = "Guest Customer"
            customer_email = "Unknown"
        
        transaction_data.append({
            'customer_name': customer_name,
            'product_name': transaction.product.name,
            'amount': transaction.amount,
            'quantity': transaction.quantity,
            'timestamp': transaction.timestamp,
        })

    # Render the template with transaction data
    return render(request, 'transaction.html', {'transactions': transaction_data})

def AnalysisView(request):
    qs = Bill.objects.all()
    x = [item.timestamp for item in qs]
    y = [item.total for item in qs]
    chart = get_plot(x, y)
    return render(request, 'analysis.html', {"chart": chart})

def bill_view(request):
    return render(request, 'billing.html')

def get_product_suggestions(request):
    search_term = request.GET.get('search', '')
    products = Product.objects.filter(name__icontains=search_term)[:5]
    suggestions = [{'name': product.name, 'price': float(product.price)} for product in products]
    return JsonResponse(suggestions, safe=False)

logger = logging.getLogger(__name__)
@csrf_exempt
@require_POST
def generate_bill(request):
    if request.method == 'POST':
        try:
            # Parse customer details
            customer_name = request.POST.get('customer_name')
            customer_email = request.POST.get('customer_email')
            phone_no = request.POST.get('phone_no')
            address = request.POST.get('address')

            # Parse products list
            try:
                products_data = json.loads(request.POST.get('products', '[]'))
            except json.JSONDecodeError:
                return JsonResponse({'success': False, 'error': 'Invalid JSON format for products.'}, status=400)

            if not products_data:
                return JsonResponse({'success': False, 'error': 'No products provided.'}, status=400)

            # Parse grand total
            grand_total_str = request.POST.get('grand_total', '0.0')
            try:
                grand_total = float(grand_total_str.replace('$', '').strip())
            except ValueError:
                return JsonResponse({'success': False, 'error': 'Invalid grand total format.'}, status=400)

            # Check if customer exists in the database
            try:
                customer = Customer.objects.get(cust_email=customer_email)
            except Customer.DoesNotExist:
                # Create a temporary customer record
                customer = Customer.objects.create(
                    cust_name=customer_name,
                    cust_email=customer_email,
                    phone_no=phone_no,
                    address=address
                )

            # Create a bill
            bill = Bill.objects.create(
                customer=customer,
                total=grand_total
            )

            # Save each product as a transaction
            for product in products_data:
                try:
                    product_instance = Product.objects.get(name=product['name'])
                except Product.DoesNotExist:
                    return JsonResponse({'success': False, 'error': f'Product "{product["name"]}" not found.'}, status=400)

                # Create a transaction record
                Transaction.objects.create(
                    bill=bill,
                    product=product_instance,
                    quantity=product['quantity'],
                    amount=product['subtotal']
                )

            # Prepare and send the email
            send_bill_email(bill)  # Pass the bill object directly

            return JsonResponse({
                'success': True,
                'customer_email': customer_email,
                'bill_content': f'Bill #{bill.id} - Total: ${grand_total:.2f}'
            })
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=500)
    else:
        return JsonResponse({'success': False, 'error': 'Invalid request method.'}, status=405)

def send_bill_email(bill):
    customer = bill.customer
    transactions = bill.transaction_set.all()
    bill_details = {
        'bill': bill,
        'customer': customer,
        'transactions': transactions,
    }

    email_subject = f"Your Bill Details - Bill #{bill.id}"
    email_body = render_to_string('emaildesign.html', bill_details)
    
    send_mail(
        subject=email_subject,
        message='',
        from_email='grochubbusiness@example.com',
        recipient_list=[customer.cust_email],
        html_message=email_body,
    )

def get_monthly_income(request):
    monthly_income_data = Transaction.objects.annotate(
        month=TruncMonth('timestamp')
    ).values('month').annotate(
        total_income=Sum(F('quantity') * F('product__price'))
    ).order_by('month')

    labels = [item['month'].strftime('%B %Y') for item in monthly_income_data]
    data = [item['total_income'] for item in monthly_income_data]

    return JsonResponse({'labels': labels, 'data': data})

def get_real_time_customers(request):
    start_time = timezone.now() - timedelta(days=1)
    real_time_customer_data = Transaction.objects.filter(timestamp__gte=start_time).values(
        'timestamp').annotate(customer_count=Count('id')).order_by('timestamp')

    labels = [item['timestamp'].strftime('%H:%M') for item in real_time_customer_data]
    data = [item['customer_count'] for item in real_time_customer_data]

    return JsonResponse({'labels': labels, 'data': data})

@csrf_exempt
def remove_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    product.delete()
    return JsonResponse({'success': True, 'message': 'Product removed successfully'})

def remove_customer(request, email):
    # Get the customer object
    customer = get_object_or_404(Customer, cust_email=email)
    
    # Delete the customer
    customer.delete()

    # Redirect to the customer list or any other page after deletion
    return redirect('customers_list')  # Replace 'customers_list' with your actual redirect target


def get_daily_customer_buying(request):
    start_time = timezone.now() - timedelta(days=1)
    daily_customer_buying_data = Transaction.objects.filter(
        timestamp__gte=start_time
    ).annotate(
        hour=TruncHour('timestamp')
    ).values('hour').annotate(
        customer_count=Count('id')
    ).order_by('hour')

    labels = [item['hour'].strftime('%H:%M') for item in daily_customer_buying_data]
    data = [item['customer_count'] for item in daily_customer_buying_data]

    if not labels:
        labels = ['No Data']
        data = [0]

    return JsonResponse({'labels': labels, 'data': data})

