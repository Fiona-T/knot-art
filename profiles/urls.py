"""URL paths for the 'profile' app (user profile)"""
from django.urls import path
from . import views


urlpatterns = [
    path('', views.profile, name='profile'),
    path(
        'order_history/<order_number>',
        views.previous_order_detail,
        name='previous_order_detail'
        ),
    path(
        'save_market/<market_id>',
        views.add_saved_market,
        name='add_saved_market'
        ),
    path(
        'my_markets', views.show_saved_markets, name='my_markets'
        ),
]
