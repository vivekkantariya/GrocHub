from django.urls import path
from .views import homeView, manageProductView, customerPageView, loginView, add_product, transactionView, profileView, AnalysisView

urlpatterns = [
    path('', homeView, name='home'),
    path('manage-products/', manageProductView, name='manage_products'),
    path('customer-page/', customerPageView, name='customer_page'),
    path('loginpage/',loginView, name='loginpage'),
    path('productpage.html/', add_product, name='add_product'),
    path('transaction.html/', transactionView, name='transactions'),
    path('analysis.html/', AnalysisView, name='analysis'),

    path('<path:undefined_path>/', homeView, name='undefined_path'),
]
