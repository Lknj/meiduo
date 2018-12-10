from celery import Celery

# 为celery使用django配置文件进行设置
import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'demo.settings.dev'

# 创建celery应用
app = Celery('meiduo')

# 导入celery配置
app.config_from_object('celery_tasks.config')

# 自动注册celery任务
app.autodiscover_tasks([
    'celery_tasks.sms_code',
    'celery_tasks.send_active_mail'
])