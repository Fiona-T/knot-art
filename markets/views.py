"""Views for 'markets' app - craft markets seller will be attending"""
import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.views.decorators.http import require_POST
from django.http import Http404
from django.contrib import messages
from django.db.models.functions import Lower
from django.utils.safestring import mark_safe
from profiles.models import SavedMarketList, UserProfile
from .models import Market, County
from .forms import MarketForm


def show_markets(request):
    """
    Show markets with date of today or later, earliest first
    If superuser, show all markets (default ordering, latest first)
    If sort is present in the get request, then sort the markets by that
    option + pass current sorting back to context.
    If user logged in, get their saved markets list if they have one (so
    that template can show if market on their saved list or not)
    If 'county' in get request then filter results by that county.
    """
    today = datetime.date.today()
    saved_markets_list = None
    sort = None
    sort_direction = None
    county = None

    if request.user.is_superuser:
        markets = Market.objects.all()
    else:
        markets = Market.objects.filter(date__gte=today).order_by('date')
    # used in context to generate dropdown of available counties to filter by
    all_markets = markets.order_by('county')

    if request.user.is_authenticated:
        user_profile = get_object_or_404(UserProfile, user=request.user)
        try:
            saved_markets_list = get_object_or_404(
                SavedMarketList, user=user_profile
                )
        except Http404:
            saved_markets_list = None

    # GET requests for sorting
    if request.GET:
        # handles sorting
        if 'sort' in request.GET:
            sortkey = request.GET['sort']
            sort = sortkey
            # if sorting by market name, add lowercase name to model to sort
            if sortkey == 'name':
                sortkey = 'lower_name'
                markets = markets.annotate(lower_name=Lower('name'))
            # if direction is descending then reverse the sorting
            if 'direction' in request.GET:
                sort_direction = request.GET['direction']
                if sort_direction == 'desc':
                    sortkey = f'-{sortkey}'
            markets = markets.order_by(sortkey)

        # handles filtering by county
        if 'county' in request.GET:
            county = request.GET['county']
            county = get_object_or_404(County, name=county)
            markets = markets.filter(county=county)

    # used in context for select box to show the selected option
    current_sorting = f'{sort}_{sort_direction}'

    context = {
        'markets': markets,
        'saved_markets_list': saved_markets_list,
        'current_sorting': current_sorting,
        'current_county': county,
        'all_markets': all_markets,
    }
    template = 'markets/markets.html'
    return render(request, template, context)


@login_required()
def add_market(request):
    """
    Show market form for admin user to add market. Raise 403 if not admin.
    Handle posting of form, show success/error messages.
    """
    if not request.user.is_superuser:
        raise PermissionDenied()
    if request.method == 'POST':
        form = MarketForm(request.POST, request.FILES)
        if form.is_valid():
            market = form.save()
            messages.success(
                request, f'New market: "{market}" added!'
                )
            return redirect('markets')
        else:
            messages.error(
                request,
                'Market not added. Please check the form for errors and '
                're-submit.'
                )
    else:
        form = MarketForm()
    context = {
        'form': form,
    }
    template = 'markets/add_market.html'
    return render(request, template, context)


@login_required()
def edit_market(request, market_id):
    """
    Show form for admin user to edit existing market. Raise 403 if not admin.
    Handle posting of form, show success/error messages.
    Show alert if editing a market with a past date.
    """
    if not request.user.is_superuser:
        raise PermissionDenied()
    market = get_object_or_404(Market, pk=market_id)
    if request.method == 'POST':
        form = MarketForm(request.POST, request.FILES, instance=market)
        if form.is_valid():
            market = form.save()
            messages.success(
                request,
                f'Updates to market: "{market}" saved!'
                )
            return redirect('markets')
        else:
            messages.error(
                request,
                'Market NOT updated. Please check the form for errors and '
                're-submit.'
                )
    else:
        form = MarketForm(instance=market)
        today = datetime.date.today()
        if market.date < today:
            messages.info(
                request,
                mark_safe(
                    'You\'re editing a past market. You can update the '
                    'details but if you change the date, the new date must be '
                    'a future date.<br>If you want to post details of this '
                    'market on a new date, then create a new market record '
                    'using the Add Market form.'
                )
            )

    context = {
        'market': market,
        'form': form,
    }
    template = 'markets/edit_market.html'
    return render(request, template, context)


@require_POST
@login_required
def delete_market(request, market_id):
    """
    View for admin user to delete market from front end.
    Raise 403 if not admin.
    Post request only: delete market, show success message.
    """
    if not request.user.is_superuser:
        raise PermissionDenied()
    market = get_object_or_404(Market, pk=market_id)
    market.delete()
    messages.success(
        request, f'Market: "{market}" deleted!'
        )
    return redirect('markets')
