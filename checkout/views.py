"""Views for checkout app - checkout page to complete a purchase"""
import json
from django.shortcuts import (
    render, redirect, reverse, get_object_or_404, HttpResponse
    )
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.conf import settings

import stripe

from cart.contexts import cart_contents
from products.models import Product
from .models import OrderLineItem, Order
from .forms import OrderForm


@require_POST
def cache_checkout_data(request):
    """
    Cache the data in the webhooks process from stripe_elements.js
    Before calling confirmCardPayment js, makes a post request to this view
    This view modifies the Stripe payment intent, adding cart contents to
    the metadata. Cart contents will be used by payment_intent_succeeded handler
    to find the order in the database and create it if it's not there.
    Response sent back to js - 200 means will call confirmCardPayment Stripe
    method; 400 means page will reload to show the error message.
    """
    try:
        pid = request.POST.get('client_secret').split('_secret')[0]
        stripe.api_key = settings.STRIPE_SECRET_KEY
        stripe.PaymentIntent.modify(pid, metadata={
            'cart': json.dumps(request.session.get('cart', {})),
        })
        return HttpResponse(status=200)
    except Exception as e:
        messages.error(request, 'Sorry, your payment cannot be \
            processed right now. Please try again later.')
        return HttpResponse(content=e, status=400)


def checkout(request):
    """
    Get request:
    Show the checkout page with Order form
    If nothing in cart, return to shop page with error message.
    Get stripe variables, create payment intent using secret key.
    Get client_secret back from the intent, pass it to context to confirm
    payment, along with public key which is used to create element.
    Post request:
    Create instance of order form with the data posted, if form is valid then
    for each item in the cart, get the product and create an orderlineitem
    instance, add client secret + original_cart, return to success page.
    If product doesn't exist, delete order, return cart page with error msg.
    If form not valid, display error message.
    """
    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    stripe_secret_key = settings.STRIPE_SECRET_KEY

    if request.method == 'POST':
        cart = request.session.get('cart', {})
        # form data done manually so as to leave out the save info box
        form_data = {
            'full_name': request.POST['full_name'],
            'email': request.POST['email'],
            'phone_number': request.POST['phone_number'],
            'street_address1': request.POST['street_address1'],
            'street_address2': request.POST['street_address2'],
            'town_or_city': request.POST['town_or_city'],
            'county': request.POST['county'],
            'postcode': request.POST['postcode'],
            'country': request.POST['country'],
        }
        order_form = OrderForm(form_data)
        if order_form.is_valid():
            order = order_form.save(commit=False)
            pid = request.POST.get('client_secret').split('_secret')[0]
            order.stripe_pid = pid
            order.original_cart = json.dumps(cart)
            order.save()
            for item_id, quantity in cart.items():
                try:
                    product = Product.objects.get(id=item_id)
                    order_line_item = OrderLineItem(
                        order=order,
                        product=product,
                        quantity=quantity,
                    )
                    order_line_item.save()
                except Product.DoesNotExist:
                    messages.error(request, (
                        "One of the products in your bag wasn't found in our "
                        "database. Please call us for assistance!")
                    )
                    order.delete()
                    return redirect(reverse('view_cart'))
            return redirect(
                reverse('checkout_success', args=[order.order_number])
                )
        else:
            messages.error(
                request,
                'There was an error with the information you entered into the '
                'form. Please double check your information and try again.'
                )
    else:
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


def checkout_success(request, order_number):
    """
    Show the checkout success page, pass back order so order summary can be
    displayed. Show success message, and delete cart session variable.
    """
    order = get_object_or_404(Order, order_number=order_number)
    messages.success(
        request,
        f'Order number: {order_number} successfully created! '
        f'An email will be sent to {order.email} with the order details.')
    if 'cart' in request.session:
        del request.session['cart']
    template = 'checkout/checkout_success.html'
    context = {
        'order': order,
    }
    return render(request, template, context)
