from django.shortcuts import render
from rest_framework.views import APIView
from .models import User
from rest_framework.response import Response
from rest_framework import generics
from .serializers import UserRegisterSerializer


class UsernameCountView(APIView):
    # 查询用户名个数,判断用户名是否存在
    def get(self, request, username):
        count = User.objects.filter(username=username).count()
        # 用户名存在, 响应
        return Response({
            "username": username,
            "count": count
        })


class MobileCountView(APIView):
    def get(self, request, mobile):
        # 查询手机号个数,判断手机号是存在
        count = User.objects.filter(mobile=mobile).count()
        # 响应
        return Response({
            'mobile': mobile,
            'count': count
        })


class UserRegisterView(generics.CreateAPIView):
    # 注册: 创建用户对象
    # 继承CreatAPIView, 接下来指定...
    # 创建不需要指定查询集
    # 需要指定序列化器类型

    serializer_class = UserRegisterSerializer
