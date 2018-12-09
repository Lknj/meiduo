import re

from django.conf import settings
from django_redis import get_redis_connection
from rest_framework import serializers
from itsdangerous import TimedJSONWebSignatureSerializer as TJWSS

from users.models import User
from . import constants
from .models import OauthQQ
from demo.utils import jwt_token


class QQSerializer(serializers.Serializer):
    mobile = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)
    sms_code = serializers.IntegerField(write_only=True)
    access_token = serializers.CharField(write_only=True)

    user_id = serializers.IntegerField(read_only=True)
    username = serializers.CharField(read_only=True)
    token = serializers.CharField(read_only=True)

    # 验证mobile password sms_code 与注册时一样
    def validate_mobile(self, value):
        # 格式是否正确
        if not re.match('^1[3-9]\d{9}$', value):
            raise serializers.ValidationError('手机号格式错误')
        # 是否存在
        if User.objects.filter(mobile=value).count() > 0:
            raise serializers.ValidationError('手机号已存在')
        return value

    def validate(self, attrs):
        # 获取所有请求的数据
        password = attrs.get('password')

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

    def validate_access_token(self, value):
        tjwss = TJWSS(settings.SECRET_KEY, constants.OPENID_EXPIRES)
        try:
            json = tjwss.loads(value)
        except:
            raise serializers.ValidationError("授权信息已过期")
        return json.get('openid')

    def create(self, validated_data):
        mobile = validated_data.get('mobile')
        password = validated_data.get('password')
        openid = validated_data.get('access_token')

        # 1. 根据手机号查询对象
        try:
            user = User.objects.get(mobile=mobile)
        except:
            # 3 如果未查询到,则
            # 3.1 创建新用户对象
            user = User()
            user.username = mobile
            user.mobile = mobile
            user.set_password(password)
            user.save()

            # 3.2 绑定
            qq = OauthQQ.objects.create(
                openid=openid,
                user_id=user.id
            )
            # 3.3 状态保持
            user.token = jwt_token.generate(user)

        else:

            # 2. 如果查询到,则
            # 2.1 判断密码是否正确
            if user.check_password(password):
                # 2.1.1 如果密码正确则绑定, 状态保持
                qq = OauthQQ.objects.create(
                    openid=openid,
                    user=user
                )
                user.token = jwt_token.generate(user)
            else:
                # 2.1.2 如果密码错误则提示
                raise serializers.ValidationError('密码错误')
        return user
