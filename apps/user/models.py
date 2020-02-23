from django.db import models
from django.contrib.auth.models import AbstractUser
from db.base_model import BaseModel


# Create your models here.


class User(AbstractUser, BaseModel):
    '''用户模型类'''
    img_url = models.ImageField(upload_to='user',null=True, blank=True, verbose_name='头像地址')
    img_name = models.CharField(max_length=256, null=True, blank=True, verbose_name='头像名称')
    sex = models.BooleanField(choices=((0, '男'), (1, '女'),), default=0, verbose_name='性别')
    desc = models.TextField(null=True, blank=True, default="家谱文化的传承者", verbose_name='个人简介')
    addr = models.CharField(max_length=256, null=True, blank=True, default="神州大地", verbose_name='住址')
    tele = models.CharField(max_length=11, null=True, blank=True, verbose_name='联系方式')

    class Meta:
        db_table = 'ge_user'
        verbose_name = '用户表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username
