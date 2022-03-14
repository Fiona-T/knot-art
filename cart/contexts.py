"""context processor for cart items, totals and delivery charges"""

def cart_contents(request):
    """
    context processor
    return context dictionary which will be available to all templates
    """
    cart_items = []
    total = 0
    product_count = 0

    context = {
        'cart_items': cart_items,
        'total': total,
        'product_count': product_count,
    }
    return context
