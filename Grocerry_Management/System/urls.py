from django.urls import path
from .views import homeView, product_list, customer_list, loginView, addproductView, addcustomerView, add_customerView, add_product, transactionView, AnalysisView, BillingView
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', homeView, name='home'),
    path('loginpage/',loginView, name='loginpage'),
    path('products.html/', product_list, name='productlist'),
    path('transaction.html/', transactionView, name='transactions'),
    path('addproduct.html/', addproductView, name='addproduct'),
    path('products.html/addproduct.html/', addproductView, name='addproduct'),
    path('customers.html/addcustomer.html/', addcustomerView, name='addcustomer'),
    path('addcustomer.html/', addcustomerView, name='addcustomer'),
path('customers.html/addcustomer.html/add_customer', add_customerView, name='add_customerView'),
    path('success', add_customerView, name='customers'),
    path('add_customer/', views.add_customerView, name='add_customer'),

    path('analysis.html/', AnalysisView, name='analysis'),
    path('billing.html/', BillingView, name='billing'),
    path('customers.html/', customer_list, name='customers'),

    path('<path:undefined_path>/', homeView, name='undefined_path'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)