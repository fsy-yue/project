from django.contrib import admin
from family.models import GeneBook,ImgsCatalogue, ArticleCatalogue, ZtreeCatalogue

# Register your models here.

class ImgsCatalogueInline(admin.TabularInline):
    model = ImgsCatalogue
    classes = 'collapse'

class ArticleCatalogueInline(admin.TabularInline):
    model = ArticleCatalogue
    classes = 'collapse'

class ZtreeCatalogueInline(admin.TabularInline):
    model = ZtreeCatalogue
    classes = 'collapse'


class GeneBookAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        obj.addr = obj.province + ' ' + obj.city + ' ' + obj.district
        if obj.addr.strip() == '':
            obj.addr = '暂无'
        if obj.author == '':
            obj.author = '暂无'
        obj.save()

    fieldsets = (
        ['Main', {
            'fields': ('name', 'author','province','city','district','audit_status', ),
        }],
        ['Advance', {
            # 'classes': ('collapse',),
            'fields': ('img','grant', 'user_id', 'desc'),
        }]
    )
    # inlines = [ImgsCatalogueInline, ArticleCatalogueInline, ZtreeCatalogueInline]
    list_display = ('id', 'name', 'author', 'addr', 'audit_status', 'grant', 'user_id')
    list_per_page = 20
    ordering = ('-create_time',)
    list_editable = ['author','audit_status']
    list_display_links = ('id', 'name',)
    actions_on_top = True
    actions_on_bottom = True
    search_fields = ['name', 'author', 'addr']
    list_filter = ('user_id',)
    # readonly_fields = ('grant', 'user_id')
    # date_hierarchy = ('create_time')  # 详细时间分层筛选

class ImgsCatalogueAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'book_id')
    list_per_page = 20
    ordering = ('-create_time',)
    list_editable = ['book_id']
    list_display_links = ('id', 'name',)
    actions_on_top = True
    actions_on_bottom = True
    search_fields = ['name', 'book_id']
    list_filter = ('book_id',)
    # date_hierarchy = ('create_time')  # 详细时间分层筛选

class ArticleCatalogueAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'book_id')
    list_per_page = 20
    ordering = ('-create_time',)
    list_editable = [ 'book_id']
    list_display_links = ('id', 'name',)

    actions_on_top = True
    actions_on_bottom = True
    search_fields = ['name', 'book_id']
    list_filter = ('book_id',)
    # date_hierarchy = ('create_time')  # 详细时间分层筛选

class ZtreeCatalogueAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'book_id')
    list_per_page = 20
    ordering = ('-create_time',)
    list_editable = ['book_id']
    list_display_links = ('id', 'name',)

    actions_on_top = True
    actions_on_bottom = True
    search_fields = ['name', 'book_id']
    list_filter = ('book_id',)
    # date_hierarchy = ('create_time')  # 详细时间分层筛选

admin.site.register(GeneBook,GeneBookAdmin)
admin.site.register(ImgsCatalogue, ImgsCatalogueAdmin)
admin.site.register(ArticleCatalogue, ArticleCatalogueAdmin)
admin.site.register(ZtreeCatalogue, ZtreeCatalogueAdmin)
