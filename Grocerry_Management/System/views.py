from django.shortcuts import render

# Create your views here.
def homeView(request, undefined_path=None):
    return render(request, "home.html")

def loginView(request):
    return render(request, "loginpage.html")

def manageProductView(request):
    return render(request, "home.html", {'section': 'manage_product'})

def customerPageView(request):
    return render(request, "home.html", {'section': 'customer_page'})
