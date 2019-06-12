from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('verification', views.verification, name='verification'),
    path('account_info', views.operate_account_info, name='account_info'),
    path('registration', views.registration, name='registration'),
]