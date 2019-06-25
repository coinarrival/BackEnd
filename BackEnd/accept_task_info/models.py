from django.db import models
from account_info.models import User
# from wallet_info.models import Wallet
from task_info.models import Task
# from accept_task_info.models import AcceptTask

# Create your models here.
class AcceptTask(models.Model):
    # acceptTaskID = models.AutoField(unique=True, primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    isFinished = models.BooleanField()
    answer = models.CharField(max_length=300, null=True)