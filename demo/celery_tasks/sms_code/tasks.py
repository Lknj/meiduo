from celery_tasks.main import app


@app.task(name="send_sms_code")
def send_sms_code(code):
    # 定义方法,封装耗时代码
    print(code)













# import logging
#
# from celery_tasks.main import app
# import sys
# sys.path.append('/home/python/Desktop/meiduo/demo/demo')
# from utils.ytx_sdk.sms import CCP
#
# logger = logging.getLogger("django")
#
#
# @app.task(name='send_sms_code')
# def send_sms_code(mobile, code, expires, template_id):
#     """
#     发送短信验证码
#     :param mobile: 手机号
#     :param code: 验证码
#     :param expires: 有效期
#     :return: None
#     """
#
#     try:
#         # result = CCP.send_template_sms(mobile, [code, expires], template_id)
#         result = 0
#         print(code)
#     except Exception as e:
#         logger.error("发送验证码短信[异常][ mobile: %s, message: %s ]" % (mobile, e))
#     else:
#         if result == 0:
#             logger.info("发送验证码短信[正常][ mobile: %s ]" % mobile)
#         else:
#             logger.warning("发送验证码短信[失败][ mobile: %s ]" % mobile)


