"""Views for cart app - view, adjust, remove items to be purchased"""
from django.shortcuts import render, redirect, reverse, HttpResponse


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


def adjust_cart(request, item_id):
    """
    Handles the form submitted from cart.html page to adjust quantity.
    If quantity greater than zero, set the new quantity, otherwise remove it.
    Overwrite cart session variable with new cart.
    Return user to cart page.
    """
    quantity = int(request.POST.get('quantity'))
    cart = request.session.get('cart', {})
    if quantity > 0:
        cart[item_id] = quantity
    else:
        cart.pop(item_id)
    request.session['cart'] = cart
    return redirect(reverse('view_cart'))


def remove_from_cart(request, item_id):
    """
    Handles the link from cart.html to remove an item (via javascript).
    Get cart from session, remove item, update cart session variable.
    Return success response. If error, raise server error.
    """
    try:
        cart = request.session.get('cart', {})
        cart.pop(item_id)
        request.session['cart'] = cart
        return HttpResponse(status=200)
    except Exception as error:
        return HttpResponse(status=500)
