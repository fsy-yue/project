import xadmin
from xadmin import views
from xadmin.plugins import auth

# from django.contrib import admin
from .models import Imgs, ImgsDatabase, Article, Ztree, ZtreeNode, NodePerson

# Register your models here.

from file.models import Imgs, ImgsDatabase, Article, Ztree, ZtreeNode, NodePerson

# 图片类注册
class ImgsDatabaseAdmin(auth.UserAdmin):
    list_display = ['id', 'name', 'book_id', 'catalogue_id']
    search_fields = ['name']

class ImgsAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'detail','imgsdb_id']
    search_fields = ('name', 'detail')

xadmin.site.register(ImgsDatabase, ImgsDatabaseAdmin)
xadmin.site.register(Imgs, ImgsAdmin)

# # 单个文章注册
# class ArticleAdmin(admin.ModelAdmin):
#     fields = ('name', 'book_id', 'catalogue_id', 'content')
#     list_display = ('id', 'name', 'book_id', 'catalogue_id')
#     list_per_page = 20
#     ordering = ('-create_time',)
#     list_editable = ['book_id', 'catalogue_id']
#     list_display_links = ('id','name', )
#     actions_on_top = True
#     actions_on_bottom = True
#     search_fields = ['name', 'book_id', 'catalogue_id']
#     list_filter = ('book_id', 'catalogue_id')
#     # date_hierarchy = ('create_time')  # 详细时间分层筛选
#
# admin.site.register(Article, ArticleAdmin)
#
# # 世系表注册
# class ZtreeAdmin(admin.ModelAdmin):
#     list_display = ('id', 'name', 'book_id', 'catalogue_id')
#     list_per_page = 20
#     ordering = ('-create_time',)
#     list_editable = ['book_id', 'catalogue_id']
#     list_display_links = ('id','name',)
#     actions_on_top = True
#     actions_on_bottom = True
#     search_fields = ['name', 'book_id', 'catalogue_id']
#     list_filter = ('book_id', 'catalogue_id')
#     # date_hierarchy = ('create_time')  # 详细时间分层筛选
#
# class NodePersonInline(admin.TabularInline):
#     model = NodePerson
#     classes = 'collapse'
#
# class ZtreeNodeAdmin(admin.ModelAdmin):
#     # inlines = [NodePersonInline]
#     list_display = ('id', 'name', 'pid', 'ztree_id')
#     list_per_page = 20
#     ordering = ('-create_time',)
#     list_editable = ['pid', 'ztree_id']
#     list_display_links = ('id','name',)
#     actions_on_top = True
#     actions_on_bottom = True
#     search_fields = ['name', 'pid', 'ztree_id']
#     list_filter = ('pid', 'ztree_id')
#     # date_hierarchy = ('create_time')  # 详细时间分层筛选
#
# class NodePersonAdmin(admin.ModelAdmin):
#     fieldsets = (
#         ['Main', {
#             'fields': ('last_name','first_name','other_name', 'seniority', 'sex',),
#         }],
#         ['Advance', {
#             # 'classes': ('collapse',),
#             'fields': ('spouse', 'birthdate', 'deathdate', 'desc','node_id'),
#         }]
#     )
#     list_display = ('id','last_name','first_name','other_name', 'seniority', 'sex','spouse', 'birthdate', 'deathdate')
#     list_per_page = 20
#     ordering = ('-create_time',)
#     list_editable = ['first_name','other_name', 'seniority', 'spouse']
#     list_display_links = ('id', 'last_name',)
#     actions_on_top = True
#     actions_on_bottom = True
#     search_fields = ['first_name']
#     list_filter = ('seniority', 'sex')
#     # date_hierarchy = ('create_time')  # 详细时间分层筛选
#
# admin.site.register(Ztree,ZtreeAdmin)
# admin.site.register(ZtreeNode,ZtreeNodeAdmin)
# admin.site.register(NodePerson,NodePersonAdmin)
#
#
#
#
# # 文件类注册
# class FilesDatabaseAdmin(admin.ModelAdmin):
#     list_display = ('id', 'name', 'book_id', 'catalogue_id')
#     list_per_page = 30
#     ordering = ('-create_time',)
#     list_editable = ['name', 'book_id', 'catalogue_id']
#     list_display_links = ('id',)
#     actions_on_top = True
#     actions_on_bottom = True
#     search_fields = ['name', 'book_id', 'catalogue_id']
#     # date_hierarchy = ('create_time')  # 详细时间分层筛选
#
# class FilesAdmin(admin.ModelAdmin):
#     list_display = ('id', 'name', 'filesdb_id')

# admin.site.register(FilesDatabase, FilesDatabaseAdmin)
# admin.site.register(Files, FilesAdmin)