from __future__ import absolute_import
import xadmin
from .models import UserSettings, Log
from xadmin.layout import *

from django.utils.translation import ugettext_lazy as _, ugettext

from xadmin import views


class BaseSetting(object):
    """xadmin的基本配置"""
    enable_themes = True  # 开启主题切换功能
    use_bootswath = True  # 这一行也得添加上才行

xadmin.site.register(views.BaseAdminView, BaseSetting)  # 把上面自己设定的属性注册到站点


class GlobalSetting(object):
    # 设置base_site.html的Title
    site_title = '王氏家谱管理与查询系统'
    site_footer = '王氏家谱管理与查询系统'
    menu_style = "accordion"


xadmin.site.register(views.CommAdminView, GlobalSetting)




class UserSettingsAdmin(object):
    model_icon = 'fa fa-cog'
    hidden_menu = True

xadmin.site.register(UserSettings, UserSettingsAdmin)

class LogAdmin(object):

    def link(self, instance):
        if instance.content_type and instance.object_id and instance.action_flag != 'delete':
            admin_url = self.get_admin_url('%s_%s_change' % (instance.content_type.app_label, instance.content_type.model), 
                instance.object_id)
            return "<a href='%s'>%s</a>" % (admin_url, _('Admin Object'))
        else:
            return ''
    link.short_description = ""
    link.allow_tags = True
    link.is_column = False

    list_display = ('action_time', 'user', 'ip_addr', '__str__', 'link')
    list_filter = ['user', 'action_time']
    search_fields = ['ip_addr', 'message']
    model_icon = 'fa fa-cog'

xadmin.site.register(Log, LogAdmin)





from user.models import User
from xadmin.plugins import auth

class UserAdmin(auth.UserAdmin):
    list_display = ['id', 'username', 'tele', 'email']
    readonly_fields = ['last_login', 'date_joined']
    search_fields = ('username', 'first_name', 'last_name', 'email', 'tele')
    style_fields = {'user_permissions': 'm2m_transfer', 'groups': 'm2m_transfer'}

    def get_model_form(self, **kwargs):
        # org_obj, 原始数据对象(User), 判断是否有用户
        if self.org_obj is None:
            # 添加用户表单
            self.fields = ['username', 'tele', 'is_staff']

        return super().get_model_form(**kwargs)

xadmin.site.unregister(User)  # 反注册
xadmin.site.register(User, UserAdmin)  # 自己再注册




# from file.models import Imgs, ImgsDatabase, Article, Ztree, ZtreeNode, NodePerson

# # 图片类注册
# class ImgsDatabaseAdmin(auth.UserAdmin):
#     list_display = ['id', 'name', 'book_id', 'catalogue_id']
#     search_fields = ['name']
#
# class ImgsAdmin(auth.UserAdmin):
#     list_display = ['id', 'name', 'detail','imgsdb_id']
#     search_fields = ('name', 'detail')
#
# xadmin.site.register(ImgsDatabase, ImgsDatabaseAdmin)
# xadmin.site.register(Imgs, ImgsAdmin)
