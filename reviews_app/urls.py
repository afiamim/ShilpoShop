from django.urls import path

from . import views


urlpatterns = [

    path(
        'add/<int:product_id>/',
        views.add_review,
        name='add_review'
    ),

    path(
        'product/<int:product_id>/',
        views.review_list,
        name='review_list'
    ),

    path(
        'delete/<int:id>/',
        views.delete_review,
        name='delete_review'
    ),

]