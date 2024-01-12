from django.urls import path
from .views import (
    homeView, product_list, customer_list, loginView,
    addproductView, addcustomerView, add_customerView, add_productView,
    transactionView, AnalysisView, BillingView
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

    path('transaction.html/', transactionView, name='transactions'),
    path('analysis.html/', AnalysisView, name='analysis'),
    path('billing.html/', BillingView, name='billing'),

    path('<path:undefined_path>/', homeView, name='undefined_path'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
