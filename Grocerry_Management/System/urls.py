from django.urls import path
from .views import homeView, manageProductView, customerPageView, loginView, addproductView, transactionView, AnalysisView, BillingView, customersView

urlpatterns = [
    path('', homeView, name='home'),
    path('manage-products/', manageProductView, name='manage_products'),
    path('customer-page/', customerPageView, name='customer_page'),
    path('loginpage/',loginView, name='loginpage'),
    path('productpage.html/', addproductView, name='productlist'),
    path('transaction.html/', transactionView, name='transactions'),
    path('analysis.html/', AnalysisView, name='analysis'),
    path('billing.html/', BillingView, name='billing'),
    path('customers.html/', customersView, name='customers'),

    path('<path:undefined_path>/', homeView, name='undefined_path'),
]
