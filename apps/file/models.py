from django.db import models
from tinymce.models import HTMLField
from db.base_model import BaseModel
from family.models import GeneBook, ImgsCatalogue, ArticleCatalogue, ZtreeCatalogue

# Create your models here.

# 定义图片部分
class ImgsDatabase(BaseModel):
    '''图片库信息模型类'''
    name = models.CharField(max_length=256, verbose_name='图片库名称/标题')
    book_id = models.ForeignKey(GeneBook, verbose_name='所属谱书')
    catalogue_id = models.ForeignKey(ImgsCatalogue,null=True,blank=True, default=None, verbose_name='所属目录')

    class Meta:
        db_table = 'ge_imgs_database'
        verbose_name = '图片库'
        verbose_name_plural = verbose_name

    def __str__(self):
        return str(self.name)

class Imgs(BaseModel):
    '''图像信息模型类'''
    img = models.ImageField(upload_to='imgs',null=True, default=None, verbose_name='图片地址')
    name = models.CharField(max_length=256, null=True, verbose_name='图片名称')
    # detail = models.CharField(max_length=2000, default='', verbose_name='图片描述信息')
    detail = models.TextField(default='', verbose_name='图片描述信息')
    imgsdb_id = models.ForeignKey(ImgsDatabase,null=True, default=None, verbose_name='所属图片库')

    class Meta:
        db_table = 'ge_imgs'
        verbose_name = '图片'
        verbose_name_plural = verbose_name

    def __str__(self):
        return str(self.name)

# 定义谱文部分
class FilesDatabase(BaseModel):
    '''图片库信息模型类'''
    name = models.CharField(max_length=256, verbose_name='文件库名称/标题')
    book_id = models.ForeignKey(GeneBook, null=True, default=None, verbose_name='所属谱书')
    catalogue_id = models.ForeignKey(ArticleCatalogue, null=True, blank=True, default=None,verbose_name='所属目录')

    class Meta:
        db_table = 'ge_files_database'
        verbose_name = '文件库'
        verbose_name_plural = verbose_name

    def __str__(self):
        return str(self.name)

class Files(BaseModel):
    '''文件信息模型类'''
    file = models.FileField(upload_to='files',null=True, default=None, verbose_name='图片地址')
    name = models.CharField(max_length=256, null=True, blank=True, verbose_name='文件名称')
    filesdb_id = models.ForeignKey(FilesDatabase, null=True, blank=True,default=None, verbose_name='所属文件库')
    class Meta:
        db_table = 'ge_files'
        verbose_name = '文件'
        verbose_name_plural = verbose_name

    def __str__(self):
        return str(self.name)

class Article(BaseModel):
    name = models.CharField(max_length=256, verbose_name='谱文标题')
    content = HTMLField()  # 字段类型HTMLField
    book_id = models.ForeignKey(GeneBook, null=True, default=None,verbose_name='所属谱书')
    catalogue_id = models.ForeignKey(ArticleCatalogue,null=True,blank=True, default=None, verbose_name='所属目录')

    class Meta:
        db_table = 'ge_article'
        verbose_name = '谱文'
        verbose_name_plural = verbose_name

    def __str__(self):
        return str(self.name)

# 定义世系部分
class Ztree(BaseModel):
    '''Ztree树形结构信息'''
    name = models.CharField(max_length=256, verbose_name='世系表名')
    book_id = models.ForeignKey(GeneBook,null=True, default=None, verbose_name='所属谱书')
    catalogue_id = models.ForeignKey(ZtreeCatalogue,null=True,blank=True, verbose_name='所属目录')
    class Meta:
        db_table = 'ge_ztree'
        verbose_name = '世系信息表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

class ZtreeNodeManager(models.Manager):
    def all(self):
        #默认查询未删除的节点信息
        #调用父类的成员语法为：super().方法名
        return super().all().filter(is_delete=False)

class ZtreeNode(BaseModel):
    '''Ztree节点信息'''
    id = models.AutoField(max_length=256, primary_key=True, verbose_name='人物id')
    name = models.CharField(max_length=256, verbose_name='人物姓名')
    pid = models.ForeignKey('self',null=True,blank=True, verbose_name='父亲')
    ztree_id = models.ForeignKey(Ztree,null=True, blank=True, on_delete=models.SET_NULL, verbose_name='所属世系表')

    objects = ZtreeNodeManager()

    class Meta:
        db_table = 'ge_ztree_node'
        verbose_name = '世系节点表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

class NodePerson(BaseModel):
    '''Ztree节点信息'''

    BROTHER_RANK_CHOICE = (
        (1, '独生子'),
        (2, '独生女'),
        (3, '第一'),
        (4, '第二'),
        (5, '第三'),
        (6, '第四'),
        (7, '第五'),
        (8, '第六'),
        (9, '第七'),
        (10, '第八'),
        (11, '第九'),
        (12, '第十'),
        (13, '第十一'),
        (14, '第十二'),
    )

    last_name = models.CharField(max_length=256, verbose_name='姓氏')
    first_name = models.CharField(max_length=256, verbose_name='名')
    other_name = models.CharField(max_length=256, null=True, blank=True, verbose_name='字')
    seniority = models.SmallIntegerField(choices=BROTHER_RANK_CHOICE,default=1, verbose_name='排行')
    sex = models.BooleanField(choices=((0, '男'), (1, '女'),), default=0, verbose_name='性别')
    spouse = models.CharField(max_length=256, null=True, blank=True,verbose_name='配偶')
    birthdate = models.DateField(null=True, blank=True,verbose_name='出生日期')
    deathdate = models.DateField(null=True,blank=True, verbose_name='死亡日期')
    desc = models.TextField(null=True, blank=True,verbose_name='人物简介')
    node_id = models.OneToOneField(ZtreeNode,null=True, blank=True,  verbose_name='对应世系节点')

    class Meta:
        db_table = 'ge_node_person'
        verbose_name = '世系节点人物表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.last_name + self.first_name