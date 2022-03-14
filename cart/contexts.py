"""context processor for cart items, totals and delivery charges"""
from decimal import Decimal
from django.conf import settings


def cart_contents(request):
    """
    context processor
    return context dictionary which will be available to all templates
    calculates delivery charge based on threshold in settings.py and amt
    of spend left to get free delivery
    """
    cart_items = []
    total = 0
    product_count = 0

    if total < settings.FREE_DELIVERY_THRESHOLD:
        delivery = total * Decimal(settings.STANDARD_DELIVERY_PERCENTAGE / 100)
        free_delivery_spend_needed = settings.FREE_DELIVERY_THRESHOLD - total
    else:
        delivery = 0
        free_delivery_spend_needed = 0

    grand_total = delivery + total

    context = {
        'cart_items': cart_items,
        'total': total,
        'product_count': product_count,
        'delivery': delivery,
        'free_delivery_spend_needed ': free_delivery_spend_needed,
        'free_delivery_threshold': settings.FREE_DELIVERY_THRESHOLD,
        'grand_total': grand_total,
    }
    return context
