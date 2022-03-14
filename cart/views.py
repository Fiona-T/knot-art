"""Views for cart app - view, adjust, remove items to be purchased"""
from django.shortcuts import render


def view_cart(request):
    """Show the items in the cart"""
    return render(request, 'cart/cart.html')
