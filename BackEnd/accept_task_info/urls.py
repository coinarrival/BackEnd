from django.urls import path

from . import views

urlpatterns = [
    # path('', views.index, name='index'),
    path('accepted_tasks', views.operate_accepted_tasks, name='accepted_tasks'),
    path('acceptance', views.operate_acceptance, name='acceptance'),
    path('acceptance_removed', views.acceptance_removed, name='acceptance_removed'),
]