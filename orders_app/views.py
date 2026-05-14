from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Order
from .forms import OrderForm
from products_app.models import Product


def apply_discount(discount_code, user, total_price):

    if not discount_code:
        return 0, ''

    try:
        from invite_app.models import ReferralProfile
        profile = ReferralProfile.objects.get(user=user)
        if not profile.discount_active:
            return 0, 'You do not have an active coupon. Invite 3 friends first!'

        if profile.discount_code != discount_code.strip().upper():
            return 0, 'Invalid coupon code. Find your code under Invite & Earn.'

        discount_amount = round(total_price * 5 / 100)
        return discount_amount, ''

    except ReferralProfile.DoesNotExist:
        return 0, 'No referral profile found.'

@login_required
def create_order(request, product_id):

    if request.user.is_staff:
        messages.error(request, 'Admin accounts cannot place orders.')
        return redirect('product_detail', id=product_id)
    product = get_object_or_404(Product, id=product_id)
    if product.stock <= 0:
        messages.error(request, 'This product is out of stock.')
        return redirect('product_detail', id=product_id)

    discount_amount      = 0
    discount_error       = ''
    user_discount_code   = ''
    user_discount_active = False

    try:
        from invite_app.models import ReferralProfile
        rp = ReferralProfile.objects.get(user=request.user)
        user_discount_code   = rp.discount_code
        user_discount_active = rp.discount_active
    except Exception:
        pass
    if request.method == 'POST':
        form = OrderForm(request.POST)

        if form.is_valid():

            quantity      = form.cleaned_data['quantity']
            discount_code = form.cleaned_data.get('discount_code', '').strip().upper()
            total_price   = product.price * quantity

            discount_amount, discount_error = apply_discount(
                discount_code, request.user, total_price
            )

            if discount_error:
                messages.error(request, discount_error)

            else:
                final_price = total_price - discount_amount

                order               = form.save(commit=False)
                order.user          = request.user
                order.product       = product
                order.total_price   = total_price
                order.discount_code   = discount_code
                order.discount_amount = discount_amount
                order.final_price     = final_price
                order.save()

                if discount_amount > 0:
                    messages.success(
                        request,
                        f'Order placed! 5% discount applied. '
                        f'You save ৳{discount_amount} — pay ৳{final_price} instead of ৳{total_price}.'
                    )
                else:
                    messages.success(request, f'Order placed for "{product.product_name}"!')

                return redirect('order_list')

    else:
        form = OrderForm()

    return render(request, 'orders_app/create_order.html', {
        'form':                form,
        'product':             product,
        'discount_amount':     discount_amount,
        'discount_error':      discount_error,
        'user_discount_code':  user_discount_code,
        'user_discount_active': user_discount_active,
    })

@login_required
def order_list(request):

    if request.user.is_staff:
        orders = Order.objects.all().order_by('-id')
    else:
        orders = Order.objects.filter(user=request.user).order_by('-id')
    return render(request, 'orders_app/order_list.html', {'orders': orders})


@login_required
def delete_order(request, id):
    order = get_object_or_404(Order, id=id)
    if order.user != request.user and not request.user.is_staff:
        messages.error(request, 'You cannot cancel this order.')
        return redirect('order_list')
    if request.method == 'POST':
        order.delete()
        messages.success(request, 'Order cancelled.')
        return redirect('order_list')
    return render(request, 'orders_app/delete.html', {'order': order})
