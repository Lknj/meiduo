from django.db import models


class AreaInfo(models.Model):
    name = models.CharField(max_length=20)
    parent = models.ForeignKey('self', related_name='subs', null=True)

    # city ===>
    # 省: city.parent
    # 区县: city.subs
    class Meta:
        db_table = 'tb_areas'