from rest_framework.response import Response
from rest_framework.views import APIView
from demo.utils.qq_sdk import OAuthQQ
from .models import OauthQQ
from itsdangerous import TimedJSONWebSignatureSerializer as TJWSS
from django.conf import settings
# from demo.settings import dev
from . import constants
from rest_framework.generics import CreateAPIView
from .serializers import QQSerializer
from demo.utils import jwt_token


class QQLoginURLView(APIView):
    def get(self, request):
        '''
        # 生成QQ授权的url地址
        :param request:
        :return:
        '''
        # 创建辅助类对象
        oauthQQ = OAuthQQ()
        # 调用方法,生成授权的地址
        login_url = oauthQQ.get_qq_login_url()
        # 响应
        return Response({'login_url': login_url})


class QQUserView(CreateAPIView):
    # 根据code获取openid
    def get(self, request):
        # 1. 获取code
        code = request.query_params.get('code')

        # 2. 获取token
        oauthQQ = OAuthQQ()
        token = oauthQQ.get_access_token(code)
        # 3. 获取openid
        openid = oauthQQ.get_openid(token)

        print(openid)
        # 4. 绑定
        try:
            # 4.1 使用openid进行查询
            qq = OauthQQ.objects.get(openid=openid)
        except:
            # 4.2 未查询到数据,则提示绑定
            tjwss = TJWSS(settings.SECRET_KEY, constants.OPENID_EXPIRES)
            json = {'openid': openid}
            data = tjwss.dumps(json)
            return Response({'access_token': data})
        else:
            # 4.3 如果有数据,说明已经授权绑定过,则使用user状态保持
            token = jwt_token.generate(qq.user)
            return Response({
                'user_id': qq.user.id,
                'username': qq.user.username,
                'token': token
            })
        pass

    # 将openid与用户绑定
    serializer_class = QQSerializer
    # def post(self, request):
    #     pass