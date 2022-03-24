"""Views for profile app - user profile"""
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import Http404
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

    orders = user_profile.orders.all().order_by('-date')
    template = 'profiles/profile.html'
    context = {
        'form': form,
        'on_profile_page': True,
        'orders': orders,
    }

    return render(request, template, context)


@login_required
def previous_order_detail(request, order_number):
    """
    If user is different to the user on the order, raise 404, otherwise
    show the details of a previous order from order history list.
    Re-using the checkout_success template as it has layout needed.
    Send 'from_profile' boolean to context, so can adjust template if true.
    """
    user_profile = get_object_or_404(UserProfile, user=request.user)
    order = get_object_or_404(Order, order_number=order_number)
    if user_profile != order.user_profile:
        raise Http404
    else:
        template = 'checkout/checkout_success.html'
        context = {
            'order': order,
            'from_profile': True,
        }
        return render(request, template, context)
