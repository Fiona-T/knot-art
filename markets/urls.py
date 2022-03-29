"""URL paths for the 'markets' app"""
from django.urls import path
from . import views


urlpatterns = [
    path('', views.show_markets, name='markets'),
]
