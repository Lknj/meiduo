from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class User(AbstractUser):
    # 增加新属性,如手机号                       不允许重复
    mobile = models.CharField(max_length=11, unique=True)
    # 新增字段,邮箱是否激活
    email_active = models.BooleanField(default=False)

    class Mate:
        db_table = 'tb_users'