"""
Django settings for demo project.

Generated by 'django-admin startproject' using Django 1.11.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import datetime

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 添加导包路径
import sys

sys.path.insert(0, os.path.join(BASE_DIR, 'apps'))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'dlaxcyhe3s2vncvr@ve=wv!zrdh85(!j$%h21g8+@z*xu)u(_+'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = [
    'api.meiduo.site',

]

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'users.apps.UsersConfig',
    'verifycations.apps.VerifycationsConfig',
    'oauth.apps.OauthConfig',
    'areas.apps.AreasConfig',
    'goods.apps.GoodsConfig',
    'contents.apps.ContentsConfig',

    # drf
    'rest_framework',
    # 处理跨域的包
    'corsheaders',
    # 富文本编辑器
    'ckeditor',
    # 富文本编辑器上传图片模块
    'ckeditor_uploader',
    # 定时任务
    'django_crontab',

]

MIDDLEWARE = [
    # 跨域,加在第一项
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

]

ROOT_URLCONF = 'demo.urls'
# print(os.path.join(BASE_DIR, 'templates'))
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')]
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'demo.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'meiduo',
        'HOST': 'localhost',
        'PORT': 3306,
        'USER': 'meiduo',
        'PASSWORD': 'meiduo',
    }
}

# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_URL = '/static/'

# 缓存
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/0",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    },
    "session": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    },
    'sms_code': {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/2",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    },
}
SESSION_ENGINE = "django.contrib.sessions.backends.cache"
SESSION_CACHE_ALIAS = "session"

# 日志
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,  # 是否禁用已经存在的日志器
    'formatters': {  # 日志信息显示的格式
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(lineno)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(module)s %(lineno)d %(message)s'
        },
    },
    'filters': {  # 对日志进行过滤
        'require_debug_true': {  # django在debug模式下才输出日志
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'handlers': {  # 日志处理方法
        'console': {  # 向终端中输出日志
            'level': 'INFO',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'file': {  # 向文件中输出日志
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(os.path.dirname(BASE_DIR), "logs/meiduo.log"),  # 日志文件的位置
            'maxBytes': 300 * 1024 * 1024,
            'backupCount': 10,
            'formatter': 'verbose'
        },
    },
    'loggers': {  # 日志器
        'django': {  # 定义了一个名为django的日志器
            'handlers': ['console', 'file'],  # 可以同时向终端与文件中输出日志
            'propagate': True,  # 是否继续传递日志信息
            'level': 'INFO',  # 日志器接收的最低日志级别
        },
    }
}

# 配置drf
REST_FRAMEWORK = {
    # 异常处理
    'EXCEPTION_HANDLER': 'utils.exceptions.exception_handler',
    # 身份认证的方式
    'DEFAULT_AUTHENTICATION_CLASSES': (
        # jwt=========客户端调用接口进行身份验证的方式
        'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
        # session=====用于admin
        'rest_framework.authentication.SessionAuthentication',
    ),
    # 分页, 但是有的地方不想用分页,所以不采用这种方法
    # 'DEFAULT_PAGINATION_CLASS': 'utils.pagination.StandardResultsSetPagination',
}

# jwt
JWT_AUTH = {
    # 过期时间
    'JWT_EXPIRATION_DELTA': datetime.timedelta(days=1),
    # 指定响应结果
    'JWT_RESPONSE_PAYLOAD_HANDLER': 'demo.utils.jwt_handler.jwt_response_handler',
    # 指定载荷数据
    'JWT_PAYLOAD_HANDLER': 'demo.utils.jwt_handler.jwt_payload_handler2',

}

# CORS跨域白名单
CORS_ORIGIN_WHITELIST = (
    'www.meiduo.site:8080',

)
CORS_ALLOW_CREDENTIALS = True  # 允许携带cookie

# 替换User模型
AUTH_USER_MODEL = 'users.User'

# 指定认证后端
AUTHENTICATION_BACKENDS = ['users.utils.MeiduoModelBackend']

# QQ登录的开发者信息
QQ_CLIENT_ID = '101474184'
QQ_CLIENT_SECRET = 'c6ce949e04e12ecc909ae6a8b09b637c'
QQ_REDIRECT_URI = 'http://www.meiduo.site:8080/oauth_callback.html'
QQ_STATE = '/'

# 邮箱服务器配置
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.163.com'
EMAIL_PORT = 25
# 发送邮件的邮箱
EMAIL_HOST_USER = 'lknj66@163.com'
# 在邮箱中设置的客户端授权密码
EMAIL_HOST_PASSWORD = 'liu808920'
# 收件人看到的发件人, 设置为公司的客服邮箱
EMAIL_FROM = '美多商城<lknj66@163.com>'
# 验证邮箱的过期时间
EMAIL_EXPIRES = 2 * 60 * 60

# DRF扩展
REST_FRAMEWORK_EXTENSIONS = {
    # 缓存时间
    'DEFAULT_CACHE_RESPONSE_TIMEOUT': 60 * 60,
    # 缓存存储
    'DEFAULT_USE_CACHE': 'default',
}

# 富文本编辑器ckeditor配置
CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': 'full',  # 工具条功能
        'height': 300,  # 编辑器高度
        # 'width': 300,  # 编辑器宽度
    },
}
CKEDITOR_UPLOAD_PATH = ''  # 上传图片保存路径，使用了FastDFS，所以此处设为''

# FDFS配置
FDFS_CLIENT = os.path.join(BASE_DIR, 'utils/fastdfs/client.conf')
FDFS_URL = 'http://image.meiduo.site:8888'
# 指定django使用的文件存储类型
DEFAOLT_FILE_STORAGE = 'demo.utils.fastdfs.fdfs_storage.FdfsStorage'


# 生成静态页面的路径
GENERATE_STATIC_DIR = os.path.join(os.path.dirname(os.path.dirname(BASE_DIR)), 'front_end_pc/')
# 定时任务
CRONJOBS = [
    # 每5分钟执行一次生成主页静态文件
    ('*/5 * * * *', 'contents.crons.generate_index_html', '>> ' + os.path.dirname(BASE_DIR) + '/logs/crontab.log')
]
# 解决crontab中文问题
CRONTAB_COMMAND_PREFIX = 'LANG_ALL=zh_cn.UTF-8'