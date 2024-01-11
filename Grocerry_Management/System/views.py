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
            return redirect('customers.html')  # Redirect to a success page
    else:
        form = CustomerForm()
    return render(request, 'addcustomer.html', {'form': form})
    
def transactionView(request):
    return render(request, 'transaction.html')

def AnalysisView(request):
    return render(request, 'analysis.html')

def BillingView(request):
    return render(request, 'billing.html')

def add_product(request):
    if request.method == 'POST':
        name = request.POST.get('manageProductName')
        price = request.POST.get('manageProductPrice')
        product = Product.objects.create(name=name, price=price)

        return JsonResponse({'id': product.id, 'name': product.name, 'price': product.price})
    else:
        return JsonResponse({'error': 'Invalid request method'})


# <!-- var xhr = new XMLHttpRequest();
#             xhr.open("GET", "{% url 'manage_products' %}", true);
#             xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
#             xhr.onreadystatechange = function () {
#                 if (xhr.readyState == 4 && xhr.status == 200) {
#                     // Reload the page to update the product list
#                     location.reload();
#                 }
#             };
# #             xhr.send("manageProductName=" + productName + "&manageProductPrice=" + productPrice); -->

# function addProduct() {
#     // Implement logic to add product to the table
#     var productName = document.getElementById('manageProductName').value;
#     var productPrice = document.getElementById('manageProductPrice').value;

#     var xhr = new XMLHttpRequest();
#     xhr.open("POST", "{% url 'productpage' %}", true);
#     xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
#     xhr.onreadystatechange = function () {
#         if (xhr.readyState == 4 && xhr.status == 200) {
#             // Reload the page to update the product list
#             location.reload();
#         }
#     };
#     xhr.send("manageProductName=" + productName + "&manageProductPrice=" + productPrice);
# }