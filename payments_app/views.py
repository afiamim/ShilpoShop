from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Payment
from .forms import PaymentForm
from orders_app.models import Order


@login_required
def payment_create(request, order_id):

    order = get_object_or_404(Order, id=order_id)

    if order.user != request.user:
        messages.error(request, 'You can only pay for your own orders.')
        return redirect('order_list')

    if Payment.objects.filter(order=order).exists():
        messages.warning(request, 'This order has already been paid.')
        return redirect('payment_list')

    if request.method == 'POST':

        form = PaymentForm(request.POST)

        if form.is_valid():

            payment                = form.save(commit=False)
            payment.order          = order
            payment.amount         = order.final_price
            payment.payment_status = 'Completed'
            payment.save()

            order.status = 'Processing'
            order.save()

            # Reset the coupon after it is used
            if order.discount_amount > 0:
                try:
                    from invite_app.models import ReferralProfile
                    rp = ReferralProfile.objects.get(user=request.user)
                    rp.reset_discount()
                except Exception:
                    pass

                messages.success(
                    request,
                    f'Payment of ৳{order.final_price} successful! '
                    f'You saved ৳{order.discount_amount} with your 5% coupon. '
                    f'Invite 3 more friends to earn your next coupon!'
                )
            else:
                messages.success(
                    request,
                    f'Payment of ৳{order.final_price} successful!'
                )

            return redirect('payment_list')

    else:
        form = PaymentForm()

    return render(request, 'payments_app/payment_form.html', {
        'form':  form,
        'order': order,
    })


@login_required
def payment_list(request):

    if request.user.is_staff:
        payments = Payment.objects.all().order_by('-id')
    else:
        payments = Payment.objects.filter(
            order__user=request.user
        ).order_by('-id')

    return render(request, 'payments_app/payment_list.html', {
        'payments': payments
    })


@login_required
def delete_payment(request, id):

    payment = get_object_or_404(Payment, id=id)

    if payment.order.user != request.user and not request.user.is_staff:
        messages.error(request, 'Permission denied.')
        return redirect('payment_list')

    if request.method == 'POST':
        payment.delete()
        messages.success(request, 'Payment record deleted.')
        return redirect('payment_list')

    return render(request, 'payments_app/delete.html', {'payment': payment})
