from django.db import models
from account_info.models import User
"""
from wallet_info.models import Wallet
from task_info.models import Task
from accept_task_info.models import AcceptTask
Create your models here.
"""

class Task(models.Model):
    taskID = models.AutoField(unique=True, primary_key=True)
    title = models.CharField(max_length=50)
    content = models.CharField(max_length=300)
    types = models.CharField(max_length=50)
    issuer = models.ForeignKey(User, on_delete=models.CASCADE)
    reward = models.FloatField()
    deadline = models.CharField(max_length=50)
    repeatTime = models.IntegerField()
    isCompleted = models.BooleanField(default=False)