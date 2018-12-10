from django.core.mail import send_mail
from celery_tasks.main import app
from django.conf import settings
from itsdangerous import TimedJSONWebSignatureSerializer as TJWSS


@app.task(name='send_active_mail')
def send_active_mail_task(to_email, user_id):
    # 将用户编号加密,再放入链接地址
    user_json = {'user_id': user_id}
    tjwss = TJWSS(settings.SECRET_KEY, settings.EMAIL_EXPIRES)
    token = tjwss.dumps(user_json)

    html_message = '<p>尊敬的用户您好！</p>' \
                   '<p>感谢您使用美多商城。</p>' \
                   '<p>您的邮箱为：%s 。请点击此链接激活您的邮箱：</p>' \
                   '<p><a href="http://www.meiduo.site:8080/success_verify_email.html?token=%s">点击激活<a></p>' % (to_email, token)
    send_mail(
        '注册激活',
        '',
        settings.EMAIL_FROM,
        [to_email],
        html_message=html_message

    )