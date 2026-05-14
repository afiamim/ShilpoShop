from django.db import migrations, models
import django.db.models.deletion
import invite_app.models
from django.conf import settings


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ReferralProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True,
                       serialize=False, verbose_name='ID')),
                ('referral_code', models.CharField(
                       default=invite_app.models.generate_referral_code,
                       max_length=20, unique=True)),
                ('discount_active', models.BooleanField(default=False)),
                ('discount_code', models.CharField(blank=True, default='', max_length=20)),
                ('total_rounds', models.IntegerField(default=0)),
                ('user', models.OneToOneField(
                       on_delete=django.db.models.deletion.CASCADE,
                       to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Invite',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True,
                       serialize=False, verbose_name='ID')),
                ('email', models.EmailField()),
                ('sent_on', models.DateField(auto_now_add=True)),
                ('status', models.CharField(
                       choices=[('pending', 'Pending'), ('joined', 'Joined')],
                       default='pending', max_length=10)),
                ('joined_on', models.DateField(blank=True, null=True)),
                ('counted', models.BooleanField(default=False)),
                ('referral_profile', models.ForeignKey(
                       on_delete=django.db.models.deletion.CASCADE,
                       related_name='invites',
                       to='invite_app.referralprofile')),
            ],
            options={
                'unique_together': {('referral_profile', 'email')},
            },
        ),
    ]
