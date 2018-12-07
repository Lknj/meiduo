from django.db import models
from demo.utils.models import BaseModel


class OauthQQ(BaseModel):
    openid = models.CharField(max_length=50)
    user = models.ForeignKey('users.User')  # 应用名.模型类名

    class Meta:
        db_table = 'tb_oauth_qq'