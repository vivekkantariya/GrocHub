from django.urls import path
from .views import (
    homeView, product_list, customer_list, loginView, 
    addproductView, addcustomerView, add_customerView, add_productView,
    transactionView, AnalysisView, bill_view, get_product_suggestions, generate_bill,
    get_monthly_income, get_real_time_customers, remove_product , remove_customer, get_daily_customer_buying
)
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('', homeView, name='home'),
    path('loginpage/', loginView, name='loginpage'),
    path('products.html', product_list, name='product_list'), 
    path('remove_product/<int:product_id>/', views.remove_product, name='remove_product'),
    path('remove_customer/<str:email>/', views.remove_customer, name='remove_customer'),
    path('edit_product/<int:product_id>/', views.edit_product, name='edit_product'),
    path('customers.html', customer_list, name='customer_list'),  
    path('addproduct.html', addproductView, name='addproduct'),  
    path('addcustomer.html', addcustomerView, name='addcustomer'),  
    path('products.html/addproduct.html', add_productView, name='add_productView'),  
    path('customers.html/addcustomer.html', add_customerView, name='add_customerView'),  
    path('transaction.html', transactionView, name='transactions'),  
    path('analysis.html', AnalysisView, name='analysis'),  
    path('billing.html', bill_view, name='billing'),  
    path('download_bill/<int:bill_id>/', views.download_bill, name='download_bill'),
    path('generate_bill/', views.generate_bill, name='generate_bill'),
    path('get_monthly_income/', get_monthly_income, name='get_monthly_income'),
    path('get_real_time_customers/', get_real_time_customers, name='get_real_time_customers'),
    path('get_daily_customer_buying/', get_daily_customer_buying, name='get_daily_customer_buying'),
    path('get_product_suggestions/', get_product_suggestions, name='get_product_suggestions'),
    path('send_bill_email/', views.send_bill_email, name='send_bill_email'),
    path('customers/<int:customer_id>/', views.customer_detail, name='customer_detail'),
    path('customers/<int:customer_id>/', views.customer_detail, name='customer_detail'),
    # path('stock/', views.stock_view, name='stock'),  # Stock page
    path('<path:undefined_path>/', views.homeView, name='home'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
