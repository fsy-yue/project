from django.contrib import admin
from file.models import Imgs, ImgsDatabase, Files, FilesDatabase, Article, Ztree, ZtreeNode, NodePerson


# Register your models here.

# 图片类注册
class ImgsDatabaseAdmin(admin.ModelAdmin):
    # listdisplay设置要显示在列表中的字段（id字段是Django模型的默认主键）
    list_display = ('id', 'name', 'book_id', 'catalogue_id')
    # list_per_page设置每页显示多少条记录，默认是100条
    list_per_page = 30
    # ordering设置默认排序字段，负号表示降序排序
    ordering = ('-create_time',)
    # list_editable 设置默认可编辑字段，在列表里就可以编辑
    list_editable = ['book_id', 'catalogue_id']
    # fk_fields 设置显示外键字段
    # fk_fields = ['book_id','catalogue_id']
    # 设置哪些字段可以点击进入编辑界面
    list_display_links = ('id','name', )
    # 列表顶部，设置为False不在顶部显示，默认为True。
    actions_on_top = True
    # 列表底部，设置为False不在底部显示，默认为False。
    actions_on_bottom = True
    # 搜索字段
    search_fields = ['name','book_id', 'catalogue_id']
    # 筛选
    list_filter = ('book_id', 'catalogue_id')
    # date_hierarchy = ('create_time')   # 详细时间分层筛选

class ImgsAdmin(admin.ModelAdmin):
    list_display = ('id', 'name','detail','imgsdb_id')
    list_per_page = 20
    ordering = ('-create_time',)
    list_editable = ['imgsdb_id']
    list_display_links = ('id','name',)
    actions_on_top = True
    actions_on_bottom = True
    search_fields = ['name', 'detail']
    list_filter = ('imgsdb_id',)
    # date_hierarchy = ('create_time')  # 详细时间分层筛选

admin.site.register(ImgsDatabase, ImgsDatabaseAdmin)
admin.site.register(Imgs, ImgsAdmin)

# 单个文章注册
class ArticleAdmin(admin.ModelAdmin):
    fields = ('name', 'book_id', 'catalogue_id', 'content')
    list_display = ('id', 'name', 'book_id', 'catalogue_id')
    list_per_page = 20
    ordering = ('-create_time',)
    list_editable = ['book_id', 'catalogue_id']
    list_display_links = ('id','name', )
    actions_on_top = True
    actions_on_bottom = True
    search_fields = ['name', 'book_id', 'catalogue_id']
    list_filter = ('book_id', 'catalogue_id')
    # date_hierarchy = ('create_time')  # 详细时间分层筛选

admin.site.register(Article, ArticleAdmin)

class ZtreeNodeInline(admin.TabularInline):
    model = ZtreeNode
    extra = 5 #默认显示条目的数量

# 世系表注册
class ZtreeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'book_id', 'catalogue_id')
    list_per_page = 20
    ordering = ('-create_time',)
    list_editable = ['book_id', 'catalogue_id']
    list_display_links = ('id','name',)
    actions_on_top = True
    actions_on_bottom = True
    search_fields = ['name', 'book_id', 'catalogue_id']
    list_filter = ('book_id', 'catalogue_id')
    # inlines = [ZtreeNodeInline,]


class ZtreeNodeAdmin(admin.ModelAdmin):
    # inlines = [NodePersonInline]
    list_display = ('id', 'name', 'pid', 'ztree_id')
    list_per_page = 20
    ordering = ('-create_time',)
    list_editable = ['pid', 'ztree_id']
    list_display_links = ('id','name',)
    actions_on_top = True
    actions_on_bottom = True
    search_fields = ['name', 'pid', 'ztree_id']
    list_filter = ('pid', 'ztree_id')
    # date_hierarchy = ('create_time')  # 详细时间分层筛选

class NodePersonAdmin(admin.ModelAdmin):
    fieldsets = (
        ['Main', {
            'fields': ('last_name','first_name','other_name', 'seniority', 'sex',),
        }],
        ['Advance', {
            # 'classes': ('collapse',),
            'fields': ('spouse', 'birthdate', 'deathdate', 'desc','node_id'),
        }]
    )
    list_display = ('id','last_name','first_name','other_name', 'seniority', 'sex','spouse', 'birthdate', 'deathdate')
    list_per_page = 20
    ordering = ('-create_time',)
    list_editable = ['first_name','other_name', 'seniority', 'spouse']
    list_display_links = ('id', 'last_name',)
    actions_on_top = True
    actions_on_bottom = True
    search_fields = ['first_name']
    list_filter = ('seniority', 'sex')
    # date_hierarchy = ('create_time')  # 详细时间分层筛选

admin.site.register(Ztree,ZtreeAdmin)
admin.site.register(ZtreeNode,ZtreeNodeAdmin)
admin.site.register(NodePerson,NodePersonAdmin)




# 文件类注册
class FilesDatabaseAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'book_id', 'catalogue_id')
    list_per_page = 30
    ordering = ('-create_time',)
    list_editable = ['name', 'book_id', 'catalogue_id']
    list_display_links = ('id',)
    actions_on_top = True
    actions_on_bottom = True
    search_fields = ['name', 'book_id', 'catalogue_id']
    # date_hierarchy = ('create_time')  # 详细时间分层筛选

class FilesAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'filesdb_id')

# admin.site.register(FilesDatabase, FilesDatabaseAdmin)
# admin.site.register(Files, FilesAdmin)