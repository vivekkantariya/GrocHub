from django.urls import path
from .views import homeView, manageProductView, customerPageView

urlpatterns = [
    path('', homeView, name='home'),
    path('manage-products/', manageProductView, name='manage_products'),
    path('customer-page/', customerPageView, name='customer_page'),
    # Add a catch-all pattern to redirect to homeView for any other URL
    path('<path:undefined_path>/', homeView, name='undefined_path'),
]
