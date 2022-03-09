"""Views for products app - shop pages, product admin"""
from django.shortcuts import render, get_object_or_404
from django.http import Http404
from .models import Product


def show_products(request):
    """
    View to display the products in shop
    Only active products are shown, unless user is superuser.
    """
    if request.user.is_superuser:
        products = Product.objects.all()
    else:
        products = Product.objects.filter(is_active=True)

    context = {
        'products': products,
    }
    return render(request, 'products/products.html', context)


def product_details(request, product_id):
    """
    View to show individual product details from shop page
    Superuser can access the view for any products
    Other users can only access the view for active products
    """
    product = get_object_or_404(Product, pk=product_id)
    if not product.is_active and not request.user.is_superuser:
        raise Http404
    else:
        context = {
            'product': product,
        }
        return render(request, 'products/product_details.html', context)
