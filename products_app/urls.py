from django.urls import path
from . import views

urlpatterns = [
    path('', views.product_list,name='product_list'),
    path('<int:id>/', views.product_detail,name='product_detail'),
    path('add/', views.product_add,name='product_add'),
    path('edit/<int:id>/', views.product_edit,name='product_edit'),
    path('delete/<int:id>/', views.product_delete,name='product_delete'),
]
