from django.db import models
from tinymce.models import HTMLField
from db.base_model import BaseModel
# Create your models here.


class CultureCategory(BaseModel):

    name = models.CharField(max_length=256, verbose_name='文章类别')

    class Meta:
        db_table = 'ge_zculture_category'
        verbose_name = '文化类别表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name



class CultureArticle(BaseModel):

    title = models.CharField(max_length=256, verbose_name='文章标题')
    author = models.CharField(max_length=256, verbose_name='作者')
    introduce = models.TextField(null=True, verbose_name='文章导读')
    content = HTMLField()  # 字段类型HTMLField
    img = models.ImageField(upload_to='culture', verbose_name='所配图片')
    read_count = models.IntegerField(default=0, verbose_name='文章阅读量')
    category_id = models.ForeignKey(CultureCategory,null=True, blank= True, default=None, verbose_name='所属类别')


    class Meta:
        db_table = 'ge_culture_article'
        verbose_name = '文化中心文章'
        verbose_name_plural = verbose_name

    def __str__(self):
        return str(self.title)
