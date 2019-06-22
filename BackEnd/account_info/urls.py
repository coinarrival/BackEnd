from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('verification', views.verification, name='verification'),
    path('account_info', views.operate_account_info, name='account_info'),
    path('registration', views.registration, name='registration'),
    path('balance', views.get_balance, name='balance'), 
    path('task', views.operate_task, name='task'), 
    path('tasks', views.get_tasks, name='tasks'), 
]