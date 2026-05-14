from django.contrib import admin
from .models import ReferralProfile, Invite

@admin.register(ReferralProfile)
class ReferralProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'referral_code', 'discount_active', 'discount_code', 'total_rounds']

@admin.register(Invite)
class InviteAdmin(admin.ModelAdmin):
    list_display = ['referral_profile', 'email', 'status', 'sent_on', 'joined_on', 'counted']
