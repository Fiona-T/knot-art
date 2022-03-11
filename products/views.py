"""Views for products app - shop pages, product admin"""
from django.shortcuts import render, get_object_or_404
from django.http import Http404
from django.db.models import Q
from django.db.models.functions import Lower
from .models import Product, Category


def show_products(request):
    """
    View to display the products in shop
    Only active products are shown, unless user is superuser.
    Products are then filtered if there is a get request with 'q'
    Or filtered by category if get request with category
    And sorted if there is a get request with sort in it
    """
    if request.user.is_superuser:
        products = Product.objects.all()
    else:
        products = Product.objects.filter(is_active=True)

    search_term = None
    category = None
    sort = None

    # GET requests for search, categories and sorting
    if request.GET:
        # handles sorting
        if 'sort' in request.GET:
            sortkey = request.GET['sort']
            sort = sortkey
            # if sorting by product name, add lowercase name to model to sort
            if sortkey == 'name':
                sortkey = 'lower_name'
                products = products.annotate(lower_name=Lower('name'))
            # if direction is descending then reverse the sorting
            if 'direction' in request.GET:
                if request.GET['direction'] == 'desc':
                    sortkey = f'-{sortkey}'
            products = products.order_by(sortkey)

        # handles filtering by category
        if 'category' in request.GET:
            category = request.GET['category']
            category = get_object_or_404(Category, name=category)
            products = products.filter(category=category)

        # handles searches
        if 'q' in request.GET:
            search_term = request.GET['q']
            matches_search = Q(
                name__icontains=search_term
                ) | Q(
                    description__icontains=search_term
                    )
            products = products.filter(matches_search)

    context = {
        'products': products,
        'search_term': search_term,
        'current_category': category,
    }
    return render(request, 'products/products.html', context)


def product_details(request, product_id):
    """
    View to show individual product details from shop page
    Superuser can access the view for any products
    Other users can only access the view for active products
    """
    product = get_object_or_404(Product, pk=product_id)
    if not product.is_active and not request.user.is_superuser:
        raise Http404
    else:
        context = {
            'product': product,
        }
        return render(request, 'products/product_details.html', context)
