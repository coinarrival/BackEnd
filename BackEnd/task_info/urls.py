from django.urls import path

from . import views

urlpatterns = [
    # path('', views.index, name='index'),
    path('task', views.operate_task, name='task'), 
    path('tasks', views.get_tasks, name='tasks'), 
    path('task_removed', views.task_finished, name='task_finished'),
    path('created_tasks', views.operate_created_tasks, name='created_tasks'),
]