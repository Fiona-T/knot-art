"""Views for products app - shop pages, product admin"""
from django.shortcuts import render
from .models import Product


def show_products(request):
    """View to display the products in shop"""
    products = Product.objects.all()
    context = {
        'products': products,
    }
    return render(request, 'products/products.html', context)
