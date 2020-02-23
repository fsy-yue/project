from django.db import models
from db.base_model import BaseModel
from user.models import User

# Create your models here.
# 定义GeneBook的模型管理器类
class GeneBookManager(models.Manager):
    def all(self):
        #默认查询未删除的节点信息
        #调用父类的成员语法为：super().方法名
        return super().all().filter(is_delete=False)

class GeneBook(BaseModel):
    '''谱书'''
    AUDIT_STATUS_ENUM = {
        "UNPAID": 1,
        "UNSEND": 2,
        "UNRECEIVED": 3,
        "UNCOMMENT": 4,
        "FINISHED": 5
    }

    AUDIT_STATUS = {
        1: '未发布',
        2: '审核中',
        3: '已发布',
        4: '审核不通过',
    }

    AUDIT_STATUS_CHOICES = (
        (1, '未发布'),
        (2, '审核中'),
        (3, '已发布'),
        (4, '审核不通过'),
    )

    name = models.CharField(max_length=256, verbose_name='谱书名')
    desc = models.TextField(max_length=256, null=True, blank=True, verbose_name='谱书简介')
    img = models.ImageField(upload_to='family', null=True, blank=True,  verbose_name='谱书封面存储地址')
    img_name = models.CharField(max_length=256, null=True, blank=True,default=None,verbose_name='谱书封面')
    author = models.CharField(max_length=256, blank=True, default=None, verbose_name='修撰者')
    addr = models.CharField(max_length=256,blank=True, default=None, verbose_name='所属地区')
    province = models.CharField(max_length=256,blank=True, default=None, verbose_name='省')
    city = models.CharField(max_length=256,blank=True, default=None, verbose_name='市')
    district = models.CharField(max_length=256,blank=True, default=None, verbose_name='县/区')
    grant = models.BooleanField(choices=((0, '公开'), (1, '私密'),), default=0,verbose_name='权限')
    audit_status = models.SmallIntegerField(choices=AUDIT_STATUS_CHOICES, default=1,verbose_name='谱书状态')
    user_id = models.ForeignKey(User, null=True, blank=True, default=None, verbose_name='所属用户')
    read_count = models.IntegerField(default=0, verbose_name='文章阅读量')

    objects = GeneBookManager()

    class Meta:
        db_table = 'ge_gene_book'
        verbose_name = '1.0谱书信息表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

# 定义目录
class ImgsCatalogue(BaseModel):
    name = models.CharField(max_length=256, verbose_name='图像目录名')
    book_id = models.ForeignKey('GeneBook', verbose_name='所属谱书')

    class Meta:
        db_table = 'ge_imgs_catalogue'
        verbose_name = '1.1图像目录表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

class ArticleCatalogue(BaseModel):
    name = models.CharField(max_length=256, verbose_name='普文目录名')
    book_id = models.ForeignKey('GeneBook', verbose_name='所属谱书')

    class Meta:
        db_table = 'ge_article_catalogue'
        verbose_name = '1.2谱文目录表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

class ZtreeCatalogue(BaseModel):
    name = models.CharField(max_length=256, verbose_name='世系目录名')
    book_id = models.ForeignKey('GeneBook', verbose_name='所属谱书')

    class Meta:
        db_table = 'ge_ztree_catalogue'
        verbose_name = '1.3世系目录表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name
