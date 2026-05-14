from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import CartItem
from products_app.models import Product
from orders_app.models import Order

# Create your views here.
@login_required
def cart_view(request):
    if request.user.is_staff:
        messages.error(request, 'Admin accounts do not have a cart.')
        return redirect('product_list')

    cart_items = CartItem.objects.filter(user=request.user)
    total = sum(item.subtotal for item in cart_items)

    return render(request, 'cart_app/cart.html', {
        'cart_items': cart_items,
        'total': total
    })

@login_required
def add_to_cart(request, product_id):
    if request.user.is_staff:
        messages.error(request, 'Admin accounts cannot add items to cart.')
        return redirect('product_list')

    product = get_object_or_404(Product, id=product_id)
    existing = CartItem.objects.filter(user=request.user, product=product).first()
    current_count = CartItem.objects.filter(user=request.user).count()

    if existing:
        existing.quantity += 1
        existing.save()
        messages.success(request, f'Updated quantity for "{product.product_name}" in cart.')
    elif current_count >= 2:
        messages.warning(request, 'Cart is full. You can only add 2 different products at a time.')
    else:
        CartItem.objects.create(user=request.user, product=product, quantity=1)
        messages.success(request, f'"{product.product_name}" added to cart!')

    return redirect('cart_view')

@login_required
def remove_from_cart(request, item_id):

    item = get_object_or_404(CartItem, id=item_id, user=request.user)
    name = item.product.product_name
    item.delete()
    messages.success(request, f'"{name}" removed from cart.')

    return redirect('cart_view')

@login_required
def checkout(request):

    if request.user.is_staff:
        messages.error(request, 'Admin accounts cannot checkout.')
        return redirect('product_list')

    cart_items = CartItem.objects.filter(user=request.user)

    if not cart_items.exists():
        messages.warning(request, 'Your cart is empty!')
        return redirect('cart_view')

    for item in cart_items:
        order = Order(
            user=request.user,
            product=item.product,
            quantity=item.quantity,
        )
        order.save()
        order.final_price = order.total_price
        order.save()

    cart_items.delete()
    messages.success(request, 'Order placed successfully! Check your orders.')
    return redirect('order_list')
