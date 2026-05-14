from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .forms import RegisterForm, LoginForm, UserProfileForm
from .models import UserProfile



def register_view(request):

    if request.method == 'POST':

        form = RegisterForm(request.POST)

        if form.is_valid():

            user = form.save()

            # Create user profile
            UserProfile.objects.get_or_create(user=user)

            # Create referral profile so user can invite friends
            from invite_app.models import ReferralProfile
            ReferralProfile.objects.get_or_create(user=user)

            # Did this user register using someone's referral code?
            referral_code = request.POST.get('referral_code', '').strip().upper()
            if referral_code:
                try:
                    from invite_app.models import Invite
                    from django.utils import timezone

                    # Find who owns that code
                    ref_profile = ReferralProfile.objects.get(referral_code=referral_code)

                    # Find the matching pending invite (matched by email)
                    invite = Invite.objects.filter(
                        referral_profile=ref_profile,
                        email=user.email,
                        status='pending'
                    ).first()

                    if invite:
                        invite.status    = 'joined'
                        invite.joined_on = timezone.now().date()
                        invite.save()

                        # Check if this completes a round of 3
                        ref_profile.check_and_unlock()

                except ReferralProfile.DoesNotExist:
                    pass
                except Exception:
                    pass

            login(request, user)
            messages.success(request, f'Welcome to ShilpoShop, {user.username}!')
            return redirect('home')

    else:
        form = RegisterForm()

    return render(request, 'users_app/register.html', {'form': form})


# Login
def login_view(request):

    if request.method == 'POST':

        form = LoginForm(request.POST)

        if form.is_valid():

            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user     = authenticate(request, username=username, password=password)

            if user:
                login(request, user)
                return redirect('home')
            else:
                messages.error(request, 'Incorrect username or password.')

    else:
        form = LoginForm()

    return render(request, 'users_app/login.html', {'form': form})


# Logout
def logout_view(request):
    logout(request)
    return redirect('login')


# Profile
@login_required
def profile_view(request):

    profile, created = UserProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':

        form = UserProfileForm(request.POST, request.FILES, instance=profile)

        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated.')
            return redirect('profile')

    else:
        form = UserProfileForm(instance=profile)

    return render(request, 'users_app/profile.html', {
        'form':    form,
        'profile': profile,
    })
