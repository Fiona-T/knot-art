"""Handler for stripe webhooks, used in webhooks.py. Credit: Code Institute"""
import json
import time
from django.http import HttpResponse
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from products.models import Product
from profiles.models import UserProfile
from .models import Order, OrderLineItem


class StripeWebHookHandler:
    """Custom class to handle Stripe webhooks - used in webhooks.py"""

    def __init__(self, request):
        """
        Assign the request as an attribute, so that attributes of the
        request from stripe can be accessed
        """
        self.request = request

    def _send_confirmation_email(self, order):
        """Send order confirmation email to user. private method"""
        customer_email = order.email
        subject = render_to_string(
            'checkout/confirmation_emails/confirmation_email_subject.txt',
            {'order': order}
            )
        body = render_to_string(
            'checkout/confirmation_emails/confirmation_email_body.txt',
            {'order': order, 'contact_email': settings.DEFAULT_FROM_EMAIL}
            )
        send_mail(
            subject,
            body,
            settings.DEFAULT_FROM_EMAIL,
            [customer_email]
        )

    def handle_event(self, event):
        """
        Handle a generic/unknown/unexpected webhook event.
        Take the event from stripe, return HTTP response indicating
        it was received
        """
        return HttpResponse(
            content=f'Unhandled webhook received: {event["type"]}',
            status=200)

    def handle_payment_intent_succeeded(self, event):
        """
        Handle payment_intent.succeeded webhook from stripe.
        Which is sent when payment successful.
        If save-info from metadata is true, get user, if logged in then get
        profile, attach delivery info to it and save the profile.
        Check if the order was created (i.e. is in the database), and create
        it if not, using info from payment intent,including cart info which
        was added to intent metadata in cache_checkout_data view.
        Try to find order for 5 attempts before creating it.
        Return responses to stripe.
        """
        intent = event.data.object
        pid = intent.id
        cart = intent.metadata.cart
        save_info = intent.metadata.save_info
        billing_details = intent.charges.data[0].billing_details
        shipping_details = intent.shipping
        grand_total = round(intent.charges.data[0].amount / 100, 2)
        # set the non-required fields to none if they're blank
        for field, value in shipping_details.address.items():
            if value == "":
                shipping_details.address[field] = None
        # update the user profile if save info box was ticked
        profile = None
        username = intent.metadata.username
        if username != 'AnonymousUser':
            profile = UserProfile.objects.get(user__username=username)
            if save_info:
                profile.default_phone_number = shipping_details.phone
                profile.default_street_address1 = (
                    shipping_details.address.line1
                    )
                profile.default_street_address2 = (
                    shipping_details.address.line2
                    )
                profile.default_town_or_city = shipping_details.address.city
                profile.default_county = shipping_details.address.state
                profile.default_postcode = shipping_details.address.postal_code
                profile.default_country = shipping_details.address.country
                profile.save()
        # try to find the order for 5 attempts, break out if it is found
        order_exists = False
        attempt_number = 1
        while attempt_number <= 5:
            try:
                order = Order.objects.get(
                    full_name__iexact=shipping_details.name,
                    email__iexact=billing_details.email,
                    phone_number__iexact=shipping_details.phone,
                    country__iexact=shipping_details.address.country,
                    postcode__iexact=shipping_details.address.postal_code,
                    town_or_city__iexact=shipping_details.address.city,
                    street_address1__iexact=shipping_details.address.line1,
                    street_address2__iexact=shipping_details.address.line2,
                    county__iexact=shipping_details.address.state,
                    grand_total=grand_total,
                    original_cart=cart,
                    stripe_pid=pid,
                )
                order_exists = True
                break
            except Order.DoesNotExist:
                attempt_number += 1
                time.sleep(1)
        if order_exists:
            self._send_confirmation_email(order)
            return HttpResponse(
                    content=f'Webhook received: {event["type"]} | '
                    'SUCCESS: Verified order already in database',
                    status=200)
        # if order not found then try to create it
        else:
            order = None
            try:
                order = Order.objects.create(
                        full_name=shipping_details.name,
                        user_profile=profile,
                        email=billing_details.email,
                        phone_number=shipping_details.phone,
                        country=shipping_details.address.country,
                        postcode=shipping_details.address.postal_code,
                        town_or_city=shipping_details.address.city,
                        street_address1=shipping_details.address.line1,
                        street_address2=shipping_details.address.line2,
                        county=shipping_details.address.state,
                        original_cart=cart,
                        stripe_pid=pid,
                    )
                for item_id, quantity in json.loads(cart).items():
                    product = Product.objects.get(id=item_id)
                    order_line_item = OrderLineItem(
                        order=order,
                        product=product,
                        quantity=quantity,
                    )
                    order_line_item.save()
            except Exception as error:
                # if anything goes wrong trying to create the order,delete it
                if order:
                    order.delete()
                # send 500 to stripe, means it will try the webhook again later
                return HttpResponse(
                    content=f'Webhook received: {event["type"]} | '
                    f'ERROR: {error}',
                    status=500)
        # order must have been created, at this point in code, return response
        self._send_confirmation_email(order)
        return HttpResponse(
            content=f'Webhook received: {event["type"]} | '
            'SUCCESS: Created order in webhook',
            status=200)

    def handle_payment_intent_payment_failed(self, event):
        """
        Handle payment_intent.payment_failed webhook from stripe - when
        user's payment fails
        """
        return HttpResponse(
            content=f'Webhook received: {event["type"]}',
            status=200)
