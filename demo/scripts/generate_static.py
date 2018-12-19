#!/usr/bin/env python
# 表示查找指定命令的路径,此处查找python解释器的路径
import sys
import os

# 指定python解释器的导包路径,当前指定为manage.py同级目录
sys.path.insert(0, '../')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "demo.settings.dev")
# 读取配置,设置环境变量
import django

# django初始化
django.setup()

from goods.models import SKU
from celery_tasks.generic_detail.tasks import generate_static_sku_detail_html

if __name__ == '__main__':
    skus = SKU.objects.all()
    for sku in skus:
        generate_static_sku_detail_html(sku.id)
    print('ok')
