"""Handler for stripe webhooks, used in webhooks.py"""
from django.http import HttpResponse


class StripeWebHookHandler:
    """Custom class to handle Stripe webhooks - used in webhooks.py"""

    def __init__(self, request):
        """
        Assign the request as an attribute, so that attributes of the
        request from stripe can be accessed
        """
        self.request = request

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
        Which is sent when payment successful
        """
        return HttpResponse(
            content=f'Webhook received: {event["type"]}',
            status=200)

    def handle_payment_intent_payment_failed(self, event):
        """
        Handle payment_intent.payment_failed webhook from stripe - when
        user's payment fails
        """
        return HttpResponse(
            content=f'Webhook received: {event["type"]}',
            status=200)
