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
        'update_my_markets/<market_id>',
        views.update_saved_markets_list,
        name='update_my_markets'
        ),
    path(
        'my_markets/', views.show_saved_markets, name='my_markets'
        ),
]
