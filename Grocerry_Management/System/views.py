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
from django.http import HttpResponse, Http404
from django.shortcuts import render
from .models import Customer
from django.template.loader import render_to_string
from django.conf import settings

def homeView(request, undefined_path=None):
    print(f"Unexpected request with undefined_path: {undefined_path}")
    return render(request, 'home.html')

def loginView(request):
    return render(request, "login.html")

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

def stockView(request):
    products = Product.objects.all()  # Retrieve all products from the database
    return render(request, 'stock.html', {'product': products})

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
        name = request.POST.get('name')
        price = request.POST.get('price')
        description = request.POST.get('description')  # Optional description
        measurement_unit = request.POST.get('measurement_unit')
        custom_measurement = request.POST.get('custom_measurement') if measurement_unit == 'custom' else None

        product = Product.objects.create(
            name=name,
            price=price,
            description=description,
            measurement_unit=measurement_unit,
            custom_measurement=custom_measurement
        )
        return redirect('product_list')  # Redirect to the product list page
    return render(request, 'addproduct.html')

def transactionView(request):
    start_time = timezone.now() - timedelta(days=1)

    transactions = Transaction.objects.filter(timestamp__gte=start_time)

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
            # Add detailed logging
            logger.debug(f"Received POST data: {request.POST}")
            
            customer_name = request.POST.get('customer_name')
            customer_email = request.POST.get('customer_email')
            phone_no = request.POST.get('phone_no')
            address = request.POST.get('address')
            
            products_str = request.POST.get('products', '[]')
            logger.debug(f"Raw products string: {products_str}")

            try:
                products_data = json.loads(products_str)
                logger.debug(f"Decoded products data: {products_data}")
                
                if not isinstance(products_data, list):
                    raise ValueError("Products data must be a list.")
            except (json.JSONDecodeError, ValueError) as e:
                logger.error(f"Invalid products data: {e}")
                return JsonResponse({'success': False, 'error': f'Invalid JSON format for products: {str(e)}'}, status=400)
            
            if not products_data:
                return JsonResponse({'success': False, 'error': 'No products provided.'}, status=400)

            grand_total_str = request.POST.get('grand_total', '0.0')
            try:
                grand_total = float(grand_total_str.replace('$', '').strip())
            except ValueError:
                return JsonResponse({'success': False, 'error': 'Invalid grand total format.'}, status=400)

            # Check if the customer is regular or non-regular
            try:
                customer = Customer.objects.get(cust_email=customer_email)
            except Customer.DoesNotExist:
                if not customer_name or not customer_email:
                    return JsonResponse({'success': False, 'error': 'Non-regular customer must provide valid details.'}, status=400)
                
                customer = None  # No customer in the database for non-regular

            # Create the Bill
            bill = Bill.objects.create(
                customer=customer,  # Pass customer object or None
                total=grand_total
            )

            for product in products_data:
                try:
                    product_instance = Product.objects.get(name=product['name'])
                except Product.DoesNotExist:
                    return JsonResponse({'success': False, 'error': f'Product "{product["name"]}" not found.'}, status=400)

                Transaction.objects.create(
                    bill=bill,
                    product=product_instance,
                    quantity = float(product['quantity']),
                    amount=product['subtotal']
                )

            # Send the bill email based on whether the customer is regular or not
            if customer:
                send_bill_email(bill)  # Regular customer email
            else:
                send_non_regular_customer_email(bill, customer_name, customer_email)

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
    transactions = bill.transactions.all()
    download_url = f"{settings.SITE_URL}/download_bill/{bill.id}/"
    bill_details = {
        'bill': bill,
        'customer': customer,
        'transactions': transactions,
        'download_url': download_url,
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
def send_non_regular_customer_email(bill, customer_name, customer_email):
    transactions = bill.transactions.all()
    bill_details = {
        'bill': bill,
        'customer_name': customer_name,  # Pass customer name explicitly
        'customer_email': customer_email,  # Pass customer email explicitly
        'transactions': transactions,
    }

    email_subject = f"Your Bill Details - Bill #{bill.id}"
    email_body = render_to_string('emaildesign.html', bill_details)
    
    send_mail(
        subject=email_subject,
        message='',
        from_email='grochubbusiness@example.com',
        recipient_list=[customer_email],
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
        return JsonResponse({'status': 'success'}, status=200)

def remove_customer(request, email):
    try:
        customer = Customer.objects.get(cust_email=email)
        customer.delete()
        return HttpResponse(f'Customer with email {email} removed successfully.')
    except Customer.DoesNotExist:
        raise Http404("Customer not found.")

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

def generate_pdf(bill, transactions):
    html_string = render_to_string('bill_pdf_template.html', {'bill': bill, 'transactions': transactions})
    pdf_file_path = os.path.join(settings.MEDIA_ROOT, f'bill_{bill.id}.pdf')
    HTML(string=html_string).write_pdf(pdf_file_path)
    return pdf_file_path

from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa  # Make sure this is installed
from .models import Bill, Transaction

def download_bill(request, bill_id):
    try:
        # Fetch the bill
        bill = Bill.objects.get(id=bill_id)
    except Bill.DoesNotExist:
        return HttpResponse('Bill not found', status=404)
    
    # Fetch transactions related to the bill
    transactions = Transaction.objects.filter(bill=bill)

    # Check if the bill has an associated customer
    customer = bill.customer  # Will be `None` if no customer is linked

    # Prepare customer details based on the type
    if customer:
        customer_name = customer.cust_name
        customer_email = customer.cust_email
    else:
        customer_name = "Not Provided"
        customer_email = "Not Provided"

    # Prepare context for the template
    context = {
        'bill': bill,
        'transactions': transactions,
        'customer': customer,  # Regular customer object (if present)
        'customer_name': customer_name,
        'customer_email': customer_email,
    }

    # Load the template
    template_path = 'bill_pdf_template.html'
    template = get_template(template_path)
    html = template.render(context)

    # Generate the PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="bill_{bill.id}.pdf"'

    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse('Error generating PDF', status=500)
    
    return response

def get_customer_details(request):
    email = request.GET.get('email')
    try:
        customer = Customer.objects.get(cust_email=email, customer_type=Customer.REGULAR)
        return JsonResponse({
            'success': True,
            'customer_name': customer.cust_name,
            'phone_no': customer.phone_no,
            'address': customer.address
        })
    except Customer.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'Customer not found.'}, status=404)

def stockView(request):
    return render(request, 'stock.html')

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from .models import Product
import json

@csrf_exempt  # Disable CSRF validation for the API (optional, but requires you to handle CSRF tokens on the client-side)
def edit_product(request, product_id):
    if request.method == 'PUT':
        product = get_object_or_404(Product, id=product_id)
        data = json.loads(request.body)
        product.name = data.get('name')
        product.price = data.get('price')
        product.save()
        return JsonResponse({'status': 'success'}, status=200)
    return JsonResponse({'status': 'failed'}, status=400)
