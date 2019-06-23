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
    path('task_removed', views.task_finished, name='task_finished'),
    path('accepted_tasks', views.operate_accepted_tasks, name='accepted_tasks'),
    path('created_tasks', views.operate_created_tasks, name='created_tasks'),
]