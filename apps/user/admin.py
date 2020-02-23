from django.contrib import admin
from user.models import User


admin.site.site_header = '王氏家谱管理与查询系统'
admin.site.site_title = '王氏家谱'

# Register your models here.
class UserAdmin(admin.ModelAdmin):
    # fields = ('username','password','sex', 'email', 'addr','desc' )
    fieldsets = (
        ['Main',{
            'fields': ('username','email',),
        }],
        ['Advance',{
            # 'classes': ('collapse',),
            'fields': ('sex', 'addr','desc'),
        }]
    )
    list_display = ('id', 'username', 'sex', 'email', 'addr')
    list_per_page = 20
    ordering = ('-create_time',)
    list_editable = [ 'email','addr']
    list_display_links = ('id', 'username',)
    actions_on_top = True
    actions_on_bottom = True
    search_fields = ['username', 'addr']
    list_filter = ('addr','sex')
    date_hierarchy = ('create_time')  # 详细时间分层筛选

admin.site.register(User,UserAdmin)
# admin_site.register(User,UserAdmin)
