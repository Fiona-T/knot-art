"""Views for the 'home' app - home page"""
from django.views import generic


class HomePage(generic.TemplateView):
    """Home Page view, returns index.html. Static page, no model"""
    template_name = 'home/index.html'
