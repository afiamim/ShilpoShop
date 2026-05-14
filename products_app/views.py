from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Product, Category
from .forms import ProductForm

# Create your views here.
def product_list(request):
    products = Product.objects.all()
    categories = Category.objects.all()
    cat_id = request.GET.get('category', '')
    if cat_id:
        products = products.filter(category_id=cat_id)
    return render(request, 'products_app/product_list.html', {'products': products, 'categories':  categories, 'selected_cat': cat_id, })


def product_detail(request, id):
    product = get_object_or_404(Product, id=id)
    reviews = product.review_set.all()
    return render(request, 'products_app/product_detail.html', {'product': product, 'reviews': reviews,})


@login_required
def product_add(request):
    if not request.user.is_staff:
        messages.error(request, 'Only admins can add products.')
        return redirect('product_list')
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product added successfully.')
            return redirect('product_list')
    else:
        form = ProductForm()
    return render(request, 'products_app/product_form.html', {'form': form})


@login_required
def product_edit(request, id):
    if not request.user.is_staff:
        messages.error(request, 'Only admins can edit products.')
        return redirect('product_list')
    product = get_object_or_404(Product, id=id)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product updated.')
            return redirect('product_list')
    else:
        form = ProductForm(instance=product)
    return render(request, 'products_app/product_form.html', {
        'form': form, 'product': product
    })


@login_required
def product_delete(request, id):
    if not request.user.is_staff:
        messages.error(request, 'Only admins can delete products.')
        return redirect('product_list')
    product = get_object_or_404(Product, id=id)
    if request.method == 'POST':
        product.delete()
        messages.success(request, 'Product deleted.')
        return redirect('product_list')
    return render(request, 'products_app/delete.html', {'product': product})
