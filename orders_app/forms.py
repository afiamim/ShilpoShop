from django import forms
from .models import Order

class OrderForm(forms.ModelForm):
    discount_code = forms.CharField(
        required=False,
        label='Discount Coupon Code (optional)',
        widget=forms.TextInput(attrs={'placeholder': 'e.g. DISC5-ABCDE'})
    )
    class Meta:
        model  = Order
        fields = ['quantity']
