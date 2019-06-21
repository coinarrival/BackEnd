from django.db import models
# Create your models here.
string_max_length = 200
# class account_info(models.Model):
#     username = models.CharField(max_length=string_max_length, unique=True)
#     email = models.CharField(max_length=string_max_length, unique=True)
#     phone = models.CharField(max_length=string_max_length, unique=True)
#     password = models.CharField(max_length=string_max_length)
#     avatar = models.CharField(max_length=string_max_length, default='')


class User(models.Model):
    userID = models.AutoField(unique=True, primary_key=True)
    username = models.CharField(max_length=100, unique=True)
    gender = models.CharField(max_length=30, null=True)
    email = models.CharField(max_length=50, unique=True)
    phone = models.CharField(max_length=15, unique=True)
    school = models.CharField(max_length=50, null=True)
    major = models.CharField(max_length=30, null=True)
    age = models.IntegerField(null=True)
    role = models.CharField(max_length=30, null=True)
    studentID = models.CharField(max_length=30, null=True)
    teacherID = models.CharField(max_length=30, null=True)
    grade = models.CharField(max_length=30, null=True)
    password = models.CharField(max_length=30)
    avatar = models.CharField(max_length=300, null=True)

class Wallet(models.Model):
    walletID = models.AutoField(unique=True, primary_key=True)
    balance = models.IntegerField()
    userID = models.ForeignKey(User, on_delete=models.CASCADE)

class Task(models.Model):
    taskID = models.AutoField(unique=True, primary_key=True)
    taskName = models.CharField(max_length=50)
    content = models.CharField(max_length=300)
    type = models.IntegerField()
    issuerID = models.ForeignKey(User, on_delete=models.CASCADE)
    reward = models.IntegerField()
    deadline = models.DateTimeField()
    isCompleted = models.BooleanField()
    repeatTime = models.IntegerField()

class AcceptTask(models.Model):
    acceptTaskID = models.AutoField(unique=True, primary_key=True)
    userID = models.ForeignKey(User, on_delete=models.CASCADE)
    taskID = models.ForeignKey(Task, on_delete=models.CASCADE)
    isFinished = models.BooleanField()