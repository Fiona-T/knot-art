"""Views for 'markets' app - craft markets seller will be attending"""
import datetime
from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.views.decorators.http import require_POST
from django.http import Http404
from django.contrib import messages
from django.db.models.functions import Lower
from django.utils.safestring import mark_safe
from profiles.models import SavedMarketList, UserProfile
from .models import Market, County, Comment
from .forms import MarketForm, CommentForm


def show_markets(request):
    """
    Show markets with date of today or later, earliest first
    If superuser, show all markets (default ordering, latest first)
    If sort is present in the get request, then sort the markets by that
    option + pass current sorting back to context.
    If user logged in, get their saved markets list if they have one (so
    that template can show if market on their saved list or not)
    If 'county' in get request then filter results by that county.
    If 'view' in get request then show past markets only.
    """
    today = datetime.date.today()
    saved_markets_list = None
    sort = None
    sort_direction = None
    county = None
    view = None

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

    # GET requests for sorting and filtering
    if request.GET:
        # to filter to past markets
        if 'view' in request.GET:
            view = request.GET['view']
            if view == 'past':
                markets = Market.objects.filter(date__lt=today).order_by(
                    'date')
                # to generate dropdown counties to filter by in template
                all_markets = markets.order_by('county')

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

    # used in template to determine options to show for button and sorting
    current_view = view

    # dict for context so count of saves for each market can be got in template
    markets_saves = {
        market.id: SavedMarketList.objects.filter(market__in=[market]).count()
        for market in markets
        }

    context = {
        'markets': markets,
        'saved_markets_list': saved_markets_list,
        'current_view': current_view,
        'current_sorting': current_sorting,
        'current_county': county,
        'all_markets': all_markets,
        'markets_saves': markets_saves,
    }
    template = 'markets/markets.html'
    return render(request, template, context)


def market_details(request, market_id):
    """
    View to show an individual market and the comments on that market.
    Need to also retrieve the user's saved market list if they have one,
    so that the page shows whether the market is saved or not.
    Show comment form and handle posting of the form. If user not logged
    in then raise 403 as must be logged in to post comment.
    """
    saved_markets_list = None
    market = get_object_or_404(Market, pk=market_id)
    comments = market.comments.all()
    market_saves = SavedMarketList.objects.filter(market__in=[market]).count()

    if request.user.is_authenticated:
        user_profile = get_object_or_404(UserProfile, user=request.user)
        try:
            saved_markets_list = get_object_or_404(
                SavedMarketList, user=user_profile
                )
        except Http404:
            saved_markets_list = None

    if request.method == 'POST':
        if not request.user.is_authenticated:
            raise PermissionDenied()
        else:
            form = CommentForm(request.POST)
            redirect_url = request.POST.get('redirect_url')
            if form.is_valid():
                comment = form.save(commit=False)
                comment.author = request.user
                comment.market = market
                comment.save()
                messages.success(
                    request,
                    f'Comment on: "{market}" successfully posted!'
                    )
                return redirect(redirect_url)
            else:
                messages.error(
                    request,
                    'Comment NOT posted. Please check the form for errors and '
                    're-submit.'
                    )
    else:
        form = CommentForm()

    context = {
        'market': market,
        'comments': comments,
        'form': form,
        'saved_markets_list': saved_markets_list,
        'market_saves': market_saves,
    }
    return render(request, 'markets/market_details.html', context)


@require_POST
@login_required
def delete_comment(request, comment_id):
    """
    View for user to delete a comment they posted on a market.
    Raise 403 if the user is not the user who posted the comment.
    Post request only: delete comment, show success message.
    """
    comment = get_object_or_404(Comment, pk=comment_id)
    if not request.user == comment.author:
        raise PermissionDenied()
    market = comment.market
    comment.delete()
    messages.success(
        request,
        f'Comment from {comment.created_on.strftime("%d/%m/%Y, %-I.%M %p")}'
        f' posted on "{market}" deleted!'
        )
    return redirect(reverse('market_details', args=[market.id]))


@login_required()
def edit_comment(request, comment_id):
    """
    Show form for user to edit their comment. Raise 403 if not comment author.
    Handle posting of form, show success/error messages.
    """
    comment = get_object_or_404(Comment, pk=comment_id)
    if not request.user == comment.author:
        raise PermissionDenied()
    market = comment.market
    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            comment = form.save()
            messages.success(
                request,
                f'Updates to comment originally posted on '
                f'{comment.created_on.strftime("%d/%m/%Y, %-I.%M %p")} saved!'
                f' Comment is posted on "{market}"'
                )
            return redirect(reverse('market_details', args=[market.id]))
        else:
            messages.error(
                request,
                'Comment NOT updated. Please check the form for errors and '
                're-submit.'
                )
    else:
        form = CommentForm(instance=comment)

    context = {
        'market': market,
        'form': form,
        'comment': comment,
    }
    template = 'markets/edit_comment.html'
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
