# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2019-05-10 04:14
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import tinymce.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CultureArticle',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('is_delete', models.BooleanField(default=False, verbose_name='删除标记')),
                ('title', models.CharField(max_length=100, verbose_name='文章标题')),
                ('author', models.CharField(max_length=100, verbose_name='作者')),
                ('introduce', models.TextField(null=True, verbose_name='文章导读')),
                ('content', tinymce.models.HTMLField()),
                ('img', models.ImageField(upload_to='culture', verbose_name='所配图片')),
                ('read_count', models.IntegerField(default=0, verbose_name='文章阅读量')),
            ],
            options={
                'verbose_name': '文化中心文章',
                'db_table': 'ge_culture_article',
                'verbose_name_plural': '文化中心文章',
            },
        ),
        migrations.CreateModel(
            name='CultureCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('is_delete', models.BooleanField(default=False, verbose_name='删除标记')),
                ('name', models.CharField(max_length=100, verbose_name='文章类别')),
            ],
            options={
                'verbose_name': '文化类别表',
                'db_table': 'ge_zculture_category',
                'verbose_name_plural': '文化类别表',
            },
        ),
        migrations.AddField(
            model_name='culturearticle',
            name='category_id',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='culture.CultureCategory', verbose_name='所属类别'),
        ),
    ]