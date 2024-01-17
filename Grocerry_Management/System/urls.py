from django.urls import path
from .views import (
    homeView, product_list, customer_list, loginView,
    addproductView, addcustomerView, add_customerView, add_productView,
    transactionView, AnalysisView, bill_view, get_product_suggestions, generate_bill,
    get_monthly_income, get_real_time_customers
)
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', homeView, name='home'),
    path('loginpage/', loginView, name='loginpage'),
    path('products.html/', product_list, name='productlist'),
    path('customers.html/', customer_list, name='customerslist'),
    path('addproduct.html/', addproductView, name='addproduct'),
    path('addcustomer.html/', addcustomerView, name='addcustomer'),

    path('products.html/addproduct.html/', add_productView, name='add_productView'),
    path('customers.html/addcustomer.html/', add_customerView, name='add_customerView'),

    path('transaction.html', transactionView, name='transactions'),
    path('analysis.html', AnalysisView, name='analysis'),
    path('billing.html', bill_view, name='billing'),
    path('generate_bill/', generate_bill, name='generate_bill'),

    path('get_monthly_income/', get_monthly_income, name='get_monthly_income'),
    path('get_real_time_customers/', get_real_time_customers, name='get_real_time_customers'),

    path('get_product_suggestions/', get_product_suggestions, name='get_product_suggestions'),
    path('<path:undefined_path>/', homeView, name='undefined_path'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
