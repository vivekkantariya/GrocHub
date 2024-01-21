from django.core.mail import EmailMessage
from django.shortcuts import render, redirect
from .forms import CustomerForm, ProductForm, BillForm
from .utils import get_graph, get_plot
from .models import Product, Customer
from django.core.mail import send_mail, EmailMessage
from django.shortcuts import render
from .forms import BillForm
from .models import Product, Transaction, Bill
from django.http import JsonResponse
from django.utils import timezone
from datetime import timedelta
from django.db.models import Sum
from django.db.models.functions import TruncHour
from django.db.models import F, ExpressionWrapper, DecimalField
from django.db.models.functions import TruncMonth
from django.db.models import Count
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction
from django.core.mail import send_mail
from decimal import Decimal  # Add this import statement
from django.db import transaction


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
            return redirect('product_list')  # Redirect to the correct URL
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
    qs = Bill.objects.all()
    x = [item.timestamp for item in qs]
    y = [item.total for item in qs]
    chart = get_plot(x, y)
    return render(request, 'analysis.html', {"chart": chart})


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


@csrf_exempt
@transaction.atomic
def generate_bill(request):
    if request.method == 'POST':
        form = BillForm(request.POST)
        if form.is_valid():
            # Get list of selected products
            products = request.POST.getlist('products')
            quantities = request.POST.getlist('quantity')
            grand_total = request.POST.get('grand_total', '0.00')

            # Validate product names and retrieve product details
            valid_products = []
            total_price = 0
            for product_name, quantity in zip(products, quantities):
                product = Product.objects.filter(
                    name__iexact=product_name).first()
                if product:
                    valid_products.append({
                        'name': product.name,
                        'quantity': int(quantity),
                        'price': float(product.price)
                    })
                    total_price += float(product.price) * int(quantity)
                else:
                    return JsonResponse({'success': False, 'errors': [f'"{product_name}" is not a valid value.']})

            try:
                with transaction.atomic():
                    # Process the form data and save it to the database
                    bill = form.save(commit=False)
                    bill.total = Decimal(grand_total)
                    bill.save()

                    # Create new_transaction after bill is saved
                    new_transaction = Transaction.objects.create(
                        customer_name=bill.customer_name,
                        product_purchased=product.name,
                        amount=bill.total,
                        quantity=1
                    )

            except Exception as e:
                return JsonResponse({'success': False, 'errors': [f'Error processing the transaction: {str(e)}']})

            try:
                with transaction.atomic():
                    # Send email with the bill details
                    email_subject = 'Your Bill Details'
                    email_message = f'Thank you for your purchase!\n\n'
                    email_message += f'Customer Name: {bill.customer_name}\n'
                    email_message += f'Customer Email: {bill.customer_email}\n'
                    email_message += f'Address: {bill.address}\n'
                    email_message += f'Phone Number: {bill.phone_number}\n'
                    email_message += '\nProducts Purchased:\n'
                    for product in valid_products:
                        email_message += f'{product["name"]} - Quantity: {product["quantity"]} - Price: ${product["price"]}\n'
                    email_message += f'\nGrand Total: ${total_price}\n'
                    email_message += f'Timestamp: {bill.timestamp}\n'

                    send_email(bill.customer_email,
                               email_subject, email_message)

                    # Return a JSON response with success and customer email
                    return JsonResponse({
                        'success': True,
                        'customer_email': bill.customer_email,
                        'bill_content': email_message,
                        'grand_total': float(bill.total)
                    })

            except Exception as e:
                # Handle email sending error
                return JsonResponse({'success': False, 'errors': [f'Error sending email: {str(e)}']})

        else:
            # Handle form validation errors
            return JsonResponse({'success': False, 'errors': form.errors})
    else:
        # Handle non-POST requests
        return render(request, 'home.html')


def send_email(to_email, subject, message):
    send_mail(subject, message, 'grochub1@yahoo.com',
              [to_email], fail_silently=False)


def send_email_with_attachment(to_email, subject, message):
    try:
        email = EmailMessage(
            subject, message, 'grochub1@yahoo.com', [to_email])
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
            Sum(F('quantity') * F('product_purchased'),
                output_field=DecimalField()),
            output_field=DecimalField(),
        )
    ).order_by('month')

    labels = [item['month'].strftime('%B %Y') for item in monthly_income_data]
    data = [item['total_income'] for item in monthly_income_data]

    return JsonResponse({'labels': labels, 'data': data})


def get_real_time_customers(request):
    # Get real-time customer data for the last 24 hours
    start_time = timezone.now() - timedelta(days=1)
    real_time_customer_data = Transaction.objects.filter(timestamp__gte=start_time).values(
        'timestamp').annotate(customer_count=Count('id')).order_by('timestamp')

    labels = [item['timestamp'].strftime('%H:%M')
              for item in real_time_customer_data]
    data = [item['customer_count'] for item in real_time_customer_data]

    return JsonResponse({'labels': labels, 'data': data})


def remove_product(request, product_id):
    # Get the product instance
    product = get_object_or_404(Product, id=product_id)

    # Delete the product from the database
    product.delete()

    # Return a JSON response indicating success
    return JsonResponse({'success': True, 'message': 'Product removed successfully'})


def remove_customer(request, phone_number):
    customer = get_object_or_404(Customer, phone_number=phone_number)
    customer.delete()
    return JsonResponse({'status': 'success'})


def get_daily_customer_buying(request):
    # Get real-time customer data for the last 24 hours
    start_time = timezone.now() - timedelta(days=1)
    daily_customer_buying_data = Transaction.objects.filter(
        timestamp__gte=start_time
    ).annotate(
        hour=TruncHour('timestamp')
    ).values('hour').annotate(
        customer_count=Count('id')
    ).order_by('hour')
    labels = [item['hour'].strftime('%H:%M')
              for item in daily_customer_buying_data]
    data = [item['customer_count'] for item in daily_customer_buying_data]

    # Provide a default value if data is empty
    if not labels:
        labels = ['No Data']
        data = [0]

    return JsonResponse({'labels': labels, 'data': data})
