from django.db import models
from account_info.models import User
"""
from wallet_info.models import Wallet
from task_info.models import Task
from accept_task_info.models import AcceptTask
Create your models here.
"""
class Wallet(models.Model):
    # walletID = models.AutoField(unique=True, primary_key=True)
    balance = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)