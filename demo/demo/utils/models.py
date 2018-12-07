from django.db import models


class BaseModel(models.Model):
    # auto_now_add 表示创建对象时,会设置成当前时间, 不需要手动赋值
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    # auto_now表示创建/修改对象时,会设置当前时间,不需要手动赋值
    update_time = models.DateTimeField(auto_now=True, verbose_name='修改时间')

    class Meta:
        # 当前模型类,用于封装两个时间属性,供其他模型类继承,不需要生成表,进行如下设置
        abstract = True