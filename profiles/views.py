"""Views for profile app - user profile"""
from django.shortcuts import render


def profile(request):
    """Show the user profile page"""
    template = 'profiles/profile.html'
    context = {}

    return render(request, template, context)
