from django.db import models
from django.contrib.auth.models import User
import random
import string



def generate_referral_code():
    chars  = string.ascii_uppercase + string.digits
    suffix = ''.join(random.choices(chars, k=5))
    return 'SHILPO-' + suffix


class ReferralProfile(models.Model):


    user = models.OneToOneField(User, on_delete=models.CASCADE)


    referral_code = models.CharField(
        max_length=20, unique=True, default=generate_referral_code
    )


    discount_active = models.BooleanField(default=False)
    discount_code = models.CharField(max_length=20, blank=True, default='')
    total_rounds = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.user.username} | {self.referral_code}'

    def current_round_joined(self):
        return self.invites.filter(status='joined', counted=False).count()


    def check_and_unlock(self):

        if self.discount_active:
            return

        new_joins = self.invites.filter(status='joined', counted=False)

        if new_joins.count() >= 3:

            for invite in new_joins[:3]:
                invite.counted = True
                invite.save()


            suffix = self.referral_code.split('-')[1]
            self.discount_code   = 'DISC5-' + suffix
            self.discount_active = True
            self.total_rounds   += 1
            self.save()

    def reset_discount(self):

        self.discount_active = False
        self.discount_code   = ''
        self.save()


class Invite(models.Model):

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('joined',  'Joined'),
    ]

    referral_profile = models.ForeignKey(
        ReferralProfile,
        on_delete=models.CASCADE,
        related_name='invites'
    )
    email     = models.EmailField()
    sent_on   = models.DateField(auto_now_add=True)
    status    = models.CharField(
        max_length=10, choices=STATUS_CHOICES, default='pending'
    )
    joined_on = models.DateField(null=True, blank=True)

    counted = models.BooleanField(default=False)

    class Meta:
        unique_together = ('referral_profile', 'email')

    def __str__(self):
        return f'{self.email} – {self.status}'
