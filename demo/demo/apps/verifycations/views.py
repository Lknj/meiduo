import random
from django_redis import get_redis_connection
from rest_framework.response import Response
from rest_framework.views import APIView
from . import constants
from celery_tasks.sms_code.tasks import send_sms_code


# Create your views here.
class SmsView(APIView):
    # 接收手机号发短信
    def get(self, request, mobile):
        # 链接reids, 指定caches中的键
        redis_cli = get_redis_connection('sms_code')

        # 1. 验证是否向此手机号发过短信,如果发过则返回提示
        if redis_cli.get('sms_flag_' + mobile):
            return Response({'message': '已发送'})
        # 2. 如果未发过则发短信

        # 2.1 生成6未随机数
        sms_code = random.randint(100000, 999999)
        # 2.2 将随机数保存在redis中
        # redis_cli.setex(
        #     'sms_' + mobile,
        #     constants.SMS_CODE_EXPIRES,
        #     sms_code
        # )
        # 2.3 将发送标记保存在redis中
        # redis_cli.setex(
        #     'sms_flag_' + mobile,
        #     constants.SMS_FLAG_EXPIRES,
        #     1  # 这个值无所谓,随意写一个
        # )

        # 2.2 , 2.3的优化,只与redis交互一次
        redis_pipeline = redis_cli.pipeline()  # 管道
        redis_pipeline.setex(
            'sms_' + mobile,
            constants.SMS_CODE_EXPIRES,
            sms_code
        )

        redis_pipeline.setex(
            'sms_flag_' + mobile,
            constants.SMS_FLAG_EXPIRES,
            1  # 这个值无所谓,随意写一个
        )
        redis_pipeline.execute()  # 执行
        # 2.4 发短信, 可以调用第三方短信平台
        # print(sms_code)
        send_sms_code.delay(sms_code)
        # 3. 响应

        return Response({'message': 'ok'})
