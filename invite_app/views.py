from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone

from .models import ReferralProfile, Invite
# Create your views here.
def get_or_create_profile(user):
    profile, created = ReferralProfile.objects.get_or_create(user=user)
    return profile

@login_required
def invite_home(request):
    profile = get_or_create_profile(request.user)
    invites = profile.invites.all().order_by('-sent_on')
    current_joined = profile.current_round_joined()
    return render(request, 'invite_app/invite_home.html', {'profile':profile,'invites':invites,'current_joined':current_joined,'still_needed':max(0, 3 - current_joined), })

@login_required
def send_invite(request):
    if request.method != 'POST':
        return redirect('invite_home')
    profile = get_or_create_profile(request.user)
    email   = request.POST.get('email', '').strip().lower()
    if not email or '@' not in email:
        messages.error(request, 'Please enter a valid email address.')
        return redirect('invite_home')
    if profile.invites.filter(email=email).exists():
        messages.warning(request, f'{email} has already been invited by you.')
        return redirect('invite_home')
    Invite.objects.create(referral_profile=profile, email=email)
    messages.success(request, f'Invite sent to {email}!')
    return redirect('invite_home')

@login_required
def mark_joined(request, invite_id):
    invite = get_object_or_404(Invite, id=invite_id)
    if invite.referral_profile.user != request.user:
        messages.error(request, 'You do not have permission to do this.')
        return redirect('invite_home')

    if invite.status == 'joined':
        messages.info(request, f'{invite.email} is already marked as joined.')
        return redirect('invite_home')
    invite.status    = 'joined'
    invite.joined_on = timezone.now().date()
    invite.save()
    invite.referral_profile.check_and_unlock()
    invite.referral_profile.refresh_from_db()

    if invite.referral_profile.discount_active:
        messages.success(request,
            f'3 friends joined! Your 5% discount coupon is UNLOCKED! '
            f'Use code: {invite.referral_profile.discount_code} at checkout.'
        )
    else:
        joined = invite.referral_profile.current_round_joined()
        messages.success(request,
            f'{invite.email} marked as joined. '
            f'{joined}/3 friends joined this round.'
        )

    return redirect('invite_home')

@login_required
def delete_invite(request, invite_id):
    invite = get_object_or_404(Invite, id=invite_id, referral_profile__user=request.user)
    if request.method == 'POST':
        invite.delete()
        messages.success(request, 'Invite removed.')
        return redirect('invite_home')
    return render(request, 'invite_app/delete.html', {'invite': invite})
