"""Views for checkout app - checkout page to complete a purchase"""
from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from django.conf import settings

import stripe

from cart.contexts import cart_contents
from .forms import OrderForm


def checkout(request):
    """
    Show the checkout page with Order form
    If nothing in cart, return to shop page with error message.
    Get stripe variables, create payment intent using secret key.
    Get client_secret back from the intent, pass it to context to confirm
    payment, along with public key which is used to create element.
    """
    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    stripe_secret_key = settings.STRIPE_SECRET_KEY

    cart = request.session.get('cart', {})

    # error message if nothing in cart
    if not cart:
        messages.error(
            request,
            "Can't checkout as you don't have anything in your bag at the "
            "moment! Add some items and try again."
            )
        return redirect(reverse('products'))

    # stripe total must be an integer, set api key and create intent
    stripe_total = round(cart_contents(request)['grand_total'] * 100)
    stripe.api_key = stripe_secret_key
    intent = stripe.PaymentIntent.create(
        amount=stripe_total,
        currency=settings.STRIPE_CURRENCY,
    )
    print(intent)

    order_form = OrderForm()

    # message alert if public key not set
    if not stripe_public_key:
        messages.warning(
            request,
            'Stripe public key is missing. Did you forget to set it in your '
            'environment?'
            )

    template = 'checkout/checkout.html'
    context = {
        'order_form': order_form,
        'stripe_public_key': stripe_public_key,
        'client_secret': intent.client_secret,
    }

    return render(request, template, context)
