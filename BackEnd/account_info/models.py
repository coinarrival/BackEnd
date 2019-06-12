from django.db import models
# Create your models here.
string_max_length = 200
class account_info(models.Model):
    username = models.CharField(max_length=string_max_length, unique=True)
    email = models.CharField(max_length=string_max_length, unique=True)
    phone = models.CharField(max_length=string_max_length, unique=True)
    password = models.CharField(max_length=string_max_length)
    avatar = models.CharField(max_length=string_max_length, default='')