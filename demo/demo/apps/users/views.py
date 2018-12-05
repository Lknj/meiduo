from django.shortcuts import render
from rest_framework.views import APIView
from .models import User
from rest_framework.response import Response


class UsernameCountView(APIView):
    # 查询用户名个数,判断用户名是否存在
    def get(self, request, username):
        count = User.objects.filter(username=username).count()
        # 用户名存在, 响应
        return Response({
            "username": username,
            "count": count
        })
