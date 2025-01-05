# signals.py
from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from django.contrib import messages
from django.shortcuts import redirect

@receiver(user_logged_in)
def check_if_user_is_blocked(sender, request, user, **kwargs):
    if hasattr(user, 'profile') and user.profile.blocked:
        messages.error(request, "Your account is blocked. Please contact an administrator.")
        return redirect('login') 
