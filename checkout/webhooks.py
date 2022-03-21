"""webhook view for stripe webhooks"""
from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt

import stripe

from checkout.webhook_handler import StripeWebHookHandler


@require_POST
@csrf_exempt
def webhook(request):
    """
    Listen for webhooks from Stripe - using code from Stripe, modified.
    Credit: Code Institute.
    create instance of StripeWebHookHandler, create dictionary mapping the
    webhook event types to the handler methods. Get the event type from stripe
    and look it up in the dict, using the generic handler method by default.
    Get the response from the handler method and return the response.
    """
    wh_secret = settings.STRIPE_WH_SECRET
    stripe.api_key = settings.STRIPE_SECRET_KEY
    # Get the webhook data and verify its signature
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, wh_secret
        )
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)
    # generic exception handler
    except Exception as e:
        return HttpResponse(content=e, status=400)

    handler = StripeWebHookHandler(request)
    event_map = {
        'payment_intent.succeeded': handler.handle_payment_intent_succeeded,
        'payment_intent.payment_failed': (
            handler.handle_payment_intent_payment_failed
            ),
    }
    event_type = event['type']
    event_handler = event_map.get(event_type, handler.handle_event)
    response = event_handler(event)
    return response
