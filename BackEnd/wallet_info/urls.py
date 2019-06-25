from django.urls import path

from . import views

urlpatterns = [
    # path('', views.index, name='index'),
    path('balance', views.get_balance, name='balance'), 
]