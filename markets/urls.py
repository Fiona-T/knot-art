"""URL paths for the 'markets' app"""
from django.urls import path
from . import views


urlpatterns = [
    path('', views.show_markets, name='markets'),
    path('add/', views.add_market, name='add_market'),
    path('edit/<int:market_id>/', views.edit_market, name='edit_market'),
]
