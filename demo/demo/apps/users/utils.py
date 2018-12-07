from django.contrib.auth.backends import ModelBackend
from .models import User
import re


class MeiduoModelBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        # username中可以是用户名也可以是手机号
        if re.match(r'1[3-9]\d{9}$', username):
            # 手机号
            try:
                user = User.objects.get(mobile=username)
            except:
                user = None
        else:
            # 用户名
            try:
                user = User.objects.get(username=username)

            except:
                user = None
        # 验证密码
        if user is not None:
            if not user.check_password(password):
                user = None
        return user
