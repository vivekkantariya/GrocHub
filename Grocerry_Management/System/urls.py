from django.urls import path
from .views import homeView, manageProductView, customer_list, loginView, addproductView, transactionView, AnalysisView, BillingView

from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', homeView, name='home'),
    path('manage-products/', manageProductView, name='manage_products'),
    path('home/manageproduct/', manageProductView, name='manageproducts'),
    path('loginpage/',loginView, name='loginpage'),
    path('productpage.html/', addproductView, name='productlist'),
    path('transaction.html/', transactionView, name='transactions'),
    path('analysis.html/', AnalysisView, name='analysis'),
    path('billing.html/', BillingView, name='billing'),
    path('customers.html/', customer_list, name='customers'),

    path('<path:undefined_path>/', homeView, name='undefined_path'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)