# 使用celery
from django.core.mail import send_mail  # 发送邮件
from django.conf import settings  # 引入秘钥
from django.template import loader
from celery import Celery,platforms
import time

# 在任务处理者一端添加以下几句
import os
# import django
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dailyfresh.settings")
# django.setup()

# from goods.models import GoodsType,IndexGoodsBanner,IndexPromotionBanner,IndexTypeGoodsBanner
from django_redis import get_redis_connection


# 创建一个Celery类的实例对象
app = Celery('celery_tasks.tasks', broker='redis://127.0.0.1:6379/8')
platforms.C_FORCE_ROOT = True

# 定义任务函数
@app.task
def send_register_active_email(to_email, username, token):
    '''发送激活邮件'''
    # 组织邮件信息
    subject = '王氏家谱欢迎信息'
    message = ''
    sender = settings.EMAIL_FROM
    receiver = [to_email]
    html_message = '<h1>%s, 欢迎您成为王氏家谱注册会员</h1>请点击下面链接激活您的账户<br/><a href="http://120.78.188.2:8000/user/active/%s">http://120.78.188.2:8000/user/active/%s</a>' % (
    username, token, token)
    send_mail(subject, message, sender, receiver, html_message=html_message)
    time.sleep(5)

# 定义任务函数
@app.task
def send_change_pwd_email(to_email, username, token):
    '''发送激活邮件'''
    # 组织邮件信息
    subject = '王氏家谱修改密码页面'
    message = ''
    sender = settings.EMAIL_FROM
    receiver = [to_email]
    html_message = '<h1>王氏家谱管理与查询系统</h1><h2>%s, 你好！</h2>请点击下面链接跳转到修改密码页面<br/>' \
                   '<a href="http://120.78.188.2:8000/user/change_pwd/%s">' \
                   'http://120.78.188.2:8000/user/change_pwd/%s</a>' % (username, token, token)
    print(html_message)
    send_mail(subject, message, sender, receiver, html_message=html_message)
    time.sleep(5)
