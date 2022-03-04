"""URL paths for the 'home' app (home page)"""
from django.urls import path
from . import views


urlpatterns = [
    path('', views.HomePage.as_view(), name='home'),
]
