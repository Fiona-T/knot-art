"""Views for cart app - view, adjust, remove items to be purchased"""
from django.shortcuts import render, redirect


def view_cart(request):
    """Show the items in the cart"""
    return render(request, 'cart/cart.html')


def add_to_cart(request, item_id):
    """
    Add item to the cart. Get quantity from posted form.
    Get cart from session, if not there then create cart empty dictionary.
    If item already in cart, increase quantity, otherwise add item to cart.
    Overwrite the session variable cart with new cart.
    Use 'redirect_url' hidden input in form to redirect user back to same page.
    """
    quantity = int(request.POST.get('quantity'))
    redirect_url = request.POST.get('redirect_url')
    cart = request.session.get('cart', {})
    if item_id in list(cart.keys()):
        cart[item_id] += quantity
    else:
        cart[item_id] = quantity
    request.session['cart'] = cart
    return redirect(redirect_url)
