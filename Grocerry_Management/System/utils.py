from django.db.models.functions import TruncDay, TruncWeek, TruncMonth
from django.db.models import Sum
from .models import Transaction, Bill

def get_sales_trend(period='daily'):
    # Choose appropriate truncation based on period
    if period == 'daily':
        trunc_func = TruncDay('timestamp')
    elif period == 'weekly':
        trunc_func = TruncWeek('timestamp')
    else:  # monthly
        trunc_func = TruncMonth('timestamp')
    
    # Aggregate sales data
    sales_trend = Transaction.objects.annotate(
        period=trunc_func
    ).values('period').annotate(
        total_sales=Sum('amount')
    ).order_by('period')
    
    return sales_trend

def get_top_products(top_n=5):
    top_products = Transaction.objects.values(
        'product__name'
    ).annotate(
        total_sales=Sum('amount'),
        total_quantity=Sum('quantity')
    ).order_by('-total_sales')[:top_n]
    
    return top_products

def get_revenue_trend(period='daily'):
    # Similar to sales trend, but using Bill model
    if period == 'daily':
        trunc_func = TruncDay('date')
    elif period == 'weekly':
        trunc_func = TruncWeek('date')
    else:  # monthly
        trunc_func = TruncMonth('date')
    
    revenue_trend = Bill.objects.annotate(
        period=trunc_func
    ).values('period').annotate(
        total_revenue=Sum('total')
    ).order_by('period')
    
    return revenue_trend