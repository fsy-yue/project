"""genealogy URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
import xadmin
from django.conf import settings
from django.conf.urls.static import static

#version模块自动注册需要版本控制的 Model
from xadmin.plugins import xversion

xadmin.autodiscover()
xversion.register_models()

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^xadmin/',include(xadmin.site.urls)),#添加新路由
    # url(r'^search/', include('haystack.urls')), # 全文搜索引擎
    url(r'^tinymce/', include('tinymce.urls')),  # 富文本编辑器
    url(r'^user/', include('user.urls', namespace='user')),  # 用户
    url(r'^file/', include('file.urls', namespace='file')),  # 文件处理
    url(r'^culture/', include('culture.urls', namespace='culture')),  # 文化宣传
    url(r'^family/', include('family.urls', namespace='family')),   # 谱库
    url(r'^search/', include('search.urls', namespace='search')),  # 搜索模块
]+ static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)
