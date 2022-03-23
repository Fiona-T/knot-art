"""Views for profile app - user profile"""
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import UserProfile
from .forms import UserProfileForm


@login_required
def profile(request):
    """
    Show the user profile page with form pre-populated with saved
    info.
    """
    user_profile = get_object_or_404(UserProfile, user=request.user)
    form = UserProfileForm(instance=user_profile)
    template = 'profiles/profile.html'
    context = {
        'form': form,
    }

    return render(request, template, context)
