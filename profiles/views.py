"""Views for profile app - user profile"""
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.http import Http404
from django.db.models.functions import Lower
from checkout.models import Order
from markets.models import Market
from .models import UserProfile, SavedMarketList
from .forms import UserProfileForm


@login_required
def profile(request):
    """
    Show the user profile page with form pre-populated with saved info and
    order history list. 
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


@require_POST
@login_required
def update_saved_markets_list(request, market_id):
    """
    Add or remove a market to the user's SavedMarketList:
    Get SavedMarketList for user if it exists, otherwise create it.
    If market is in the list, then remove it, then check if list is now
    empty, if it is then delete the list. If market not in list, then add it.
    Redirect to the page the user sent the request from (markets or my_markets)
    """
    user_profile = get_object_or_404(UserProfile, user=request.user)
    market = get_object_or_404(Market, pk=market_id)
    redirect_url = request.POST.get('redirect_url')

    try:
        saved_markets_list = get_object_or_404(
            SavedMarketList, user=user_profile
            )
    except Http404:
        saved_markets_list = SavedMarketList(user=user_profile)
        saved_markets_list.save()

    if market in saved_markets_list.market.all():
        saved_markets_list.market.remove(market)
        action = 'removed from'
        saved_markets_list.save()
        if not saved_markets_list.market.all().exists():
            saved_markets_list.delete()
    else:
        saved_markets_list.market.add(market)
        action = 'added to'
        saved_markets_list.save()

    messages.success(
        request, f'Market: "{market}" { action } your saved markets!'
        )
    return redirect(redirect_url)


@login_required
def show_saved_markets(request):
    """
    Displays the markets in the user's saved market list, if they have one.
    Get the saved market list, then get the markets from it (for sorting)
    If sort is present in the get request, then sort the markets by that
    option + pass current sorting back to context.
    """
    user_profile = get_object_or_404(UserProfile, user=request.user)
    sort = None
    sort_direction = None
    saved_markets = None
    try:
        saved_markets_list = get_object_or_404(
            SavedMarketList, user=user_profile
            )
        saved_markets = saved_markets_list.market.all()
    except Http404:
        saved_markets_list = None

    # GET requests for sorting
    if request.GET:
        # handles sorting
        if 'sort' in request.GET:
            sortkey = request.GET['sort']
            sort = sortkey
            # if sorting by market name, add lowercase name to sort
            if sortkey == 'name':
                sortkey = 'lower_name'
                saved_markets = saved_markets.annotate(
                    lower_name=Lower('name')
                    )
            # if direction is descending then reverse the sorting
            if 'direction' in request.GET:
                sort_direction = request.GET['direction']
                if sort_direction == 'desc':
                    sortkey = f'-{sortkey}'
            saved_markets = saved_markets.order_by(sortkey)

    # used in context for select box to show the selected option
    current_sorting = f'{sort}_{sort_direction}'

    context = {
        'saved_markets_list': saved_markets_list,
        'current_sorting': current_sorting,
        'saved_markets': saved_markets,
    }
    template = 'profiles/my_markets.html'
    return render(request, template, context)
