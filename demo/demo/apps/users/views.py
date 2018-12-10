from rest_framework.views import APIView
from .models import User
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView, RetrieveAPIView, UpdateAPIView
from .serializers import UserRegisterSerializer, UserSerializer, EmailSerializer
from rest_framework.permissions import IsAuthenticated


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


class UserRegisterView(CreateAPIView):
    # 注册: 创建用户对象
    # 继承CreatAPIView, 接下来指定...
    # 创建不需要指定查询集
    # 需要指定序列化器类型

    serializer_class = UserRegisterSerializer


class UserView(RetrieveAPIView):
    # 要求登录后再访问
    permission_classes = [IsAuthenticated]

    # 个人信息页面,显示的数据,需要获取当前显示的用户对象,而不是根据主键查询用户对象
    # queryset =
    def get_object(self):
        # 默认实现,从路径中获取pk,查询对象
        '''
        获取对象,用于retrieve/updata/destroy
        :return:
        '''
        # 默认实现,从路径中获取pk,查询对象
        # 获取当前登录的对象,而不是查询
        # 不想使用默认实现,重写此方法,如获取当前登录的用户
        return self.request.user

    serializer_class = UserSerializer


class EmailView(UpdateAPIView):
    '''
    修改当前登录用户的邮箱属性
    '''
    # 要求登录
    permission_classes = [IsAuthenticated]
    # queryset =
    # 重写get_object()方法
    def get_object(self):
        return self.request.user
    serializer_class = EmailSerializer