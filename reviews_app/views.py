from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404

from .models import Review
from .forms import ReviewForm

from products_app.models import Product


# Add Review

def add_review(request, product_id):

    product = get_object_or_404(Product, id=product_id)

    if request.method == 'POST':

        form = ReviewForm(request.POST)

        if form.is_valid():

            review = form.save(commit=False)

            review.user = request.user

            review.product = product

            review.save()

            return redirect('review_list', product_id=product.id)

    else:

        form = ReviewForm()

    return render(request, 'reviews_app/review_form.html', {
        'form': form,
        'product': product
    })


# Review List

def review_list(request, product_id):

    product = get_object_or_404(Product, id=product_id)

    reviews = Review.objects.filter(product=product)

    return render(request, 'reviews_app/review_list.html', {
        'reviews': reviews,
        'product': product
    })


# Delete Review

def delete_review(request, id):

    review = get_object_or_404(Review, id=id)

    if request.method == 'POST':

        review.delete()

        return redirect('product_list')

    return render(request, 'reviews_app/delete.html', {
        'review': review
    })