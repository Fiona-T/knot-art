"""URL paths for the 'checkout' app (checkout/payment page)"""
from django.urls import path
from . import views


urlpatterns = [
    path('', views.checkout, name='checkout'),
]