from django.urls import path
from . import views

urlpatterns = [
    path('', views.invite_home,name='invite_home'),
    path('send/', views.send_invite,name='send_invite'),
    path('joined/<int:invite_id>/', views.mark_joined,name='mark_joined'),
    path('delete/<int:invite_id>/', views.delete_invite,name='delete_invite'),
]
