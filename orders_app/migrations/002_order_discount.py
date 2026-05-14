from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='discount_code',
            field=models.CharField(blank=True, default='', max_length=30),
        ),
        migrations.AddField(
            model_name='order',
            name='discount_amount',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='order',
            name='final_price',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='order',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
