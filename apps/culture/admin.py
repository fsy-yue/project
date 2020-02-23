from django.contrib import admin
from culture.models import CultureCategory, CultureArticle

# Register your models here.
class CultureCategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_per_page = 20
    ordering = ('-create_time',)
    list_editable = ['name']
    actions_on_top = True
    actions_on_bottom = True
    search_fields = ['name']
    # date_hierarchy = ('create_time')  # 详细时间分层筛选

class CultureArticleAdmin(admin.ModelAdmin):
    fieldsets = (
        ['Main', {
            'fields': ('title', 'author', 'read_count', 'category_id'),
        }],
        ['Advance', {
            # 'classes': ('collapse',),
            'fields': ('img','introduce', 'content'),
        }]
    )
    list_display = ('id', 'title', 'author', 'read_count', 'category_id')
    list_per_page = 20
    ordering = ('-create_time',)
    list_editable = ['author', 'read_count', 'category_id']
    list_display_links = ('id', 'title', )
    actions_on_top = True
    actions_on_bottom = True
    search_fields = ['title', 'author', 'read_count']
    list_filter = ('author', 'category_id')
    # date_hierarchy = ('create_time')  # 详细时间分层筛选

admin.site.register(CultureCategory, CultureCategoryAdmin)
admin.site.register(CultureArticle, CultureArticleAdmin)