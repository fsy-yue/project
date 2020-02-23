import xadmin
from xadmin import views
from .models import User
from xadmin.plugins import auth


class UserAdmin(auth.UserAdmin):
    list_display = ['id', 'username', 'tele', 'email', 'date_joined']
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
