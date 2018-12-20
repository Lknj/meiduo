from rest_framework import status
from rest_framework.decorators import action
from rest_framework.views import APIView

from goods.models import SKU
from .models import User, Address
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView, RetrieveAPIView, UpdateAPIView, ListCreateAPIView
from .serializers import UserRegisterSerializer, UserSerializer, EmailSerializer
from rest_framework.permissions import IsAuthenticated
from .serializers import AddressCreateSerializer, HistorySerializer
from rest_framework.mixins import UpdateModelMixin
from rest_framework.viewsets import ModelViewSet
from django_redis import get_redis_connection
from goods.serializers import SKUSerializer


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


# class AddressView(UpdateModelMixin, ListCreateAPIView):
class AddressesView(ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = AddressCreateSerializer
    queryset = Address.objects.all()

    # def get_queryset(self):
    #     user = self.request.user
    #     return user.addresses.filter(is_deleted=False)

    ## 查询当期登录用户的所有收货地址
    def list(self, request, *args, **kwargs):
        # 查询当期登录用户的所有收货地址
        user = self.request.user
        addresses = user.addresses.filter(is_deleted=False)
        # addresses = self.get_queryset()
        serializer = self.get_serializer(addresses, many=True)

        return Response({
            'addresses': serializer.data,
            'limit': 5,
            'default_address_id': user.default_address_id
        })

    # def put(self, request):
    #     return self.update(request)
    # 重写destroy,设计逻辑删除
    def destroy(self, request, *args, **kwargs):
        addresses = self.get_object()
        addresses.is_deleted = True
        addresses.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(methods=["PUT"], detail=True)
    def status(self, request, pk):
        # 设置默认收货地址
        # 1. 获取当前登录的用户对象
        user = request.user
        # 2. 修改默认收货地址属性
        user.default_address_id = pk
        # 3. 保存
        user.save()
        # 响应
        return Response({'message': "OK"})

    @action(methods=["PUT"], detail=True)
    def title(self, request, pk):
        # 修改标题
        # 1. 获取当前收货地址对象
        address = self.get_object()
        # 2. 修改属性axios.put(路径,参数,回调函数)
        address.title = request.data.get('title')
        # 3. 保存
        address.save()
        # 4. 响应
        return Response({'message': 'OK'})


class HistoryView(CreateAPIView):
    # 增加,被写好了,集成自它就行了

    # def post(self, request):
    #     # 1. 接收请求
    #     # 2. 验证
    #     # 3. 保存
    #
    #     pass
    permission_classes = [IsAuthenticated]
    serializer_class = HistorySerializer

    # 查询: 从redis中获取商品编号,根据编号从mysql中查询商品数据
    def get(self, request):
        # 1. 从redis中获取商品编号
        redis_cli = get_redis_connection('history')
        key = 'history%d' % request.user.id
        sku_ids = redis_cli.lrange(key, 0, -1)
        # 从redis中读取的数据为bytes类型,需要换成int
        sku_ids = [int(sku_id) for sku_id in sku_ids]
        # 2. 根据编号从mysql中查询商品数据
        # skus = SKU.objects.filter(pk__in=sku_ids)
        skus = []
        for sku_id in sku_ids:
            skus.append(SKU.objects.get(pk=sku_id))
        serializer = SKUSerializer(skus, many=True)
        return Response(serializer.data)
