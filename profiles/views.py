"""Views for profile app - user profile"""
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from checkout.models import Order
from .models import UserProfile
from .forms import UserProfileForm


@login_required
def profile(request):
    """
    Show the user profile page with form pre-populated with saved info and
    order history list. 'on_profile_page' in context is for messages so that
    bag info is not shown in toast msg when just updating profile.
    If post request, update the profile with the data from the form.
    """
    user_profile = get_object_or_404(UserProfile, user=request.user)

    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=user_profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile information was updated.')
        else:
            messages.error(request, 'Please check the form and submit again.')
    else:
        form = UserProfileForm(instance=user_profile)

    orders = user_profile.orders.all()
    template = 'profiles/profile.html'
    context = {
        'form': form,
        'on_profile_page': True,
        'orders': orders,
    }

    return render(request, template, context)


def previous_order_detail(request, order_number):
    """
    Show the details of a previous order from order history list.
    Re-using the checkout_success template as it has layout needed.
    Send 'from_profile' boolean to context, so can change template accordingly
    """
    order = get_object_or_404(Order, order_number=order_number)
    messages.info(request, (
        f'This is a past confirmation for order number {order_number}. '
        f'A confirmation email was sent on the order date { order.date }.'
    ))
    template = 'checkout/checkout_success.html'
    context = {
        'order': order,
        'from_profile': True,
    }
    return render(request, template, context)
