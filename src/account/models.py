from wsgiref.validate import validator
from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
"""
class User(models.Model):
    username = models.CharField(max_length=32, verbose_name='유저 아이디')
    password = models.CharField(max_length=32, verbose_name='유저 비밀번호')

    def __str__(self):
        return self.username
    
    class Meta:
        db_table = 'user'
        verbose_name = '유저'
        verbose_name_plural = '유저'
"""

class User(AbstractUser):
    pass