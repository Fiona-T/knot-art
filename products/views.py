"""Views for products app - shop pages, product admin"""
from django.shortcuts import render, get_object_or_404
from .models import Product


def show_products(request):
    """View to display the products in shop"""
    products = Product.objects.filter(is_active=True)
    context = {
        'products': products,
    }
    return render(request, 'products/products.html', context)


def product_details(request, product_id):
    """View to show individual product details from shop page"""
    product = get_object_or_404(Product, pk=product_id)
    context = {
        'product': product,
    }
    return render(request, 'products/product_details.html', context)
