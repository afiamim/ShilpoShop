from django.urls import path

from . import views


urlpatterns = [

    path(
        '',
        views.payment_list,
        name='payment_list'
    ),

    path(
        'pay/<int:order_id>/',
        views.payment_create,
        name='payment_create'
    ),

    path(
        'delete/<int:id>/',
        views.delete_payment,
        name='delete_payment'
    ),

]