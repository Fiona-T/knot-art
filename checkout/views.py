"""Views for checkout app - checkout page to complete a purchase"""
from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from .forms import OrderForm


def checkout(request):
    """
    Show the checkout page with Order form
    If nothing in cart, return to shop page with error message.
    """
    cart = request.session.get('cart', {})
    if not cart:
        messages.error(
            request,
            "Can't checkout as you don't have anything in your bag at the "
            "moment! Add some items and try again."
            )
        return redirect(reverse('products'))

    order_form = OrderForm()
    template = 'checkout/checkout.html'
    context = {
        'order_form': order_form
    }

    return render(request, template, context)
