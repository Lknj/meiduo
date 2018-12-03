from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class User(AbstractUser):
    # 增加新属性,如手机号                       不允许重复
    mobile = models.CharField(max_length=11, unique=True)

    class Mate:
        db_table = 'tb_users'