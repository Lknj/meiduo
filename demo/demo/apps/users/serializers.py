from rest_framework import serializers
from .models import User
import re
from django_redis import get_redis_connection
from rest_framework_jwt.settings import api_settings


# class UserRegisterSerializer(serializers.ModelSerializer):
class UserRegisterSerializer(serializers.Serializer):
    # 使用模型类序列化器可少写代码: 定义属性,create()方法 这两个
    # 但是create()方法会把以上的字段赋给模型类,模型类里不需要存这些字段
    # 密码需要加密才能接收

    # 写代码过程中: 1.接收的某些值不存在于模型类的属性中
    # 2. 验证方法需要自己写
    # 3. 创建方法默认是将接收的值赋给属性,但是某些值不对应着属性,密码需要加密后再赋值
    # 结论: 使用Serializer

    id = serializers.IntegerField(read_only=True)
    # 新增: 输出jwt
    token = serializers.CharField(read_only=True)
    username = serializers.CharField(
        min_length=5,
        max_length=20,
        error_messages={
            'min_length': '用户名长度为5-20个字符',
            'max_length': '用户名长度为5-20个字符'
        }
    )
    password = serializers.CharField(
        min_length=8,
        max_length=20,
        error_messages={
            'min_length': '密码长度为8-20个字符',
            'max_length': '密码长度为8-20个字符'
        },
        write_only=True
    )
    password2 = serializers.CharField(write_only=True)
    mobile = serializers.CharField()
    sms_code = serializers.IntegerField(write_only=True)
    allow = serializers.BooleanField(write_only=True)

    # class Meta:
    #     model = User
    #     fields = ['username', 'password', 'mobile']

    # 定义验证方法
    def validate_username(self, value):
        # 验证用户名是否存在
        if User.objects.filter(username=value).count() > 0:
            raise serializers.ValidationError('用户名不存在')
        return value

    def validate_mobile(self, value):
        # 格式是否正确
        if not re.match('^1[3-9]\d{9}$', value):
            raise serializers.ValidationError('手机号格式错误')
        # 是否存在
        if User.objects.filter(mobile=value).count() > 0:
            raise serializers.ValidationError('手机号已存在')
        return value

    # 判断短信验证码不应该在这里写
    # def validate_sms_code(self, value):
        # redis_cli.get('sms_' + mobile) == > 返回值

    def validate_allow(self, value):
        if not value:
            raise serializers.ValidationError('请同意协议')
        return value

    def validate(self, attrs):
        # 获取所有请求的数据
        # 1.判断两个密码是否相等
        password = attrs.get('password')
        password2 = attrs.get('password2')
        if password != password2:
            raise serializers.ValidationError('两次输入的密码不同')

        # 2.判断短信验证码是否正确: 不能使用单个属性做判断
        # 因为需要获取验证,手机号两个值
        # 2.1获取请求的验证
        code_request = attrs.get('sms_code')  # 经过类型验证,完成转换,当前是int类型
        # 2.2从redis中获取验证码
        redis_cli = get_redis_connection('sms_code')
        code_redis = redis_cli.get('sms_' + attrs.get('mobile'))

        if not code_redis:
            raise serializers.ValidationError('短信验证码已过期')

        # 2.3 对比
        # 从redis中读取的数据bytes类型,需要转换为int,再做对比
        if code_request != int(code_redis):
            raise serializers.ValidationError('短信验证码错误')
        return attrs

    def create(self, validated_data):
        # User.objects.create(v1=1, v2=2) 不能用这种方法,密码需要先加密

        user = User()
        user.username = validated_data.get('username')
        user.mobile = validated_data.get('mobile')
        # 密码加密再保存
        user.set_password(validated_data.get('password'))
        user.save()

        # 注册成功 状态保持 生成jwt
        # 1.获取pyload方法
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        # 2.获取生成token的方法
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
        # 3.根据用户对象生成载荷
        payload = jwt_payload_handler(user)
        # 4.根据载荷生成token
        token = jwt_encode_handler(payload)
        # 5.输出
        user.token = token

        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'mobile', 'email', 'email_active']


class EmailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email']

    def update(self, instance, validated_data):
        # 重写update()方法,保持原有的操作不变,新增发邮件的代码
        result = super().update(instance, validated_data)
        # 发邮件

        return result