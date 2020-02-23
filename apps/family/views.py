from django.shortcuts import render
from django.http import JsonResponse
from django.views.generic import View
from django.core.cache import cache

from utils.mixin import LoginRequiredMixin,Page

from family.models import GeneBook, ImgsCatalogue, ArticleCatalogue, ZtreeCatalogue
from file.models import ImgsDatabase, FilesDatabase, Article, Ztree
from culture.models import CultureCategory,CultureArticle

from utils.fdfs.storage import FDFSStorage

# Create your views here.

# /index
class IndexView(View):
    '''首页'''
    def get(self, request):
        '''显示首页页面'''
        # 尝试从缓存中获取数据
        context = cache.get('index_page_data')

        # if context is None:
            # print('设置缓存')

            # genebooks = GeneBook.objects.filter(audit_status=3).order_by('-create_time')[:4]
            # categorys = CultureCategory.objects.all()
            # if categorys:
            #     name_first =  categorys[0].name
            #     name_second =  categorys[1].name
            #     name_third =  categorys[2].name
            #     articles_first = categorys[0].culturearticle_set.all().order_by('-create_time')[:2]
            #     articles_second = categorys[0].culturearticle_set.all().order_by('-create_time')[:12]
            #     articles_third = categorys[0].culturearticle_set.all().order_by('-create_time')[:4]
            #
            #     context = {
            #         'name_first': name_first,
            #         'name_second': name_second,
            #         'name_third': name_third,
            #         'articles_first': articles_first,
            #         'articles_second': articles_second,
            #         'articles_third': articles_third,
            #         'books': genebooks
            #     }
            # # context = {
            # #     'books': genebooks
            # # }
            # # 设置缓存
            # # key  value timeout
            # cache.set('index_page_data', context, 3600)
        genebooks = GeneBook.objects.filter(audit_status=3).order_by('-create_time')[:4]
        categorys = CultureCategory.objects.all()
        name_first = categorys[0].name
        name_second = categorys[1].name
        name_third = categorys[2].name
        articles_first = categorys[0].culturearticle_set.all().order_by('-create_time')[:2]
        articles_second = categorys[1].culturearticle_set.all().order_by('-create_time')[:12]
        articles_third = categorys[2].culturearticle_set.all().order_by('-create_time')[:4]

        context = {
            'name_first': name_first,
            'name_second': name_second,
            'name_third': name_third,
            'articles_first': articles_first,
            'articles_second': articles_second,
            'articles_third': articles_third,
            'books': genebooks
        }

        # print(context)

        return render(request, 'index.html', context)

# /family/center
class FamilyCenterView(View):
    '''家谱中心页面视图类'''
    def get(self, request):
        '''显示'''
        sort = request.GET.get('sort')
        if sort == 'intro':
            genebooks = GeneBook.objects.filter(grant=False,audit_status=3).order_by('-read_count')
        elif sort == 'new':
            genebooks = GeneBook.objects.filter(audit_status=3).order_by('-create_time')
        elif sort == 'open':
            genebooks = GeneBook.objects.filter(grant=False,audit_status=3)
        else:
            sort = 'all'
            genebooks = GeneBook.objects.filter(audit_status=3)

        page = request.GET.get('page')
        pageobj = Page(genebooks, 8, page)
        context = pageobj.paging()
        context['books'] = genebooks
        context['sort'] = sort

        return render(request, 'family_center.html',  context)

# /family/read
class FamilyReadView(LoginRequiredMixin,View):
    '''家谱中心家谱详情页面视图类'''
    def get(self, request, book_id):
        '''显示'''
        if not book_id:
            book = None
        else:
            book_id = int(book_id)
            try:
                book = GeneBook.objects.get(id=book_id)
            except GeneBook.DoesNotExist:
                book = None
        if book:
            # 若book存在
            book.img_cata = book.imgscatalogue_set.all()
            book.article_cata = book.articlecatalogue_set.all()
            book.ztree_cata = book.ztreecatalogue_set.all()
            book.imgdb_title = book.imgsdatabase_set.filter(catalogue_id=None)
            book.article_title = book.article_set.filter(catalogue_id=None)
            book.ztree_title = book.ztree_set.filter(catalogue_id=None)
            book.read_count += 1
            book.save()

        return render(request, 'family_read.html', {'book': book})

# /family/create
class FamilyCreateView(LoginRequiredMixin,View):
    '''家谱中心家谱详情页面视图类'''
    def get(self, request, book_id):
        '''显示'''
        if not book_id:
            book = None
        else:
            book_id = int(book_id)
            try:
                book = GeneBook.objects.get(id=book_id)
            except GeneBook.DoesNotExist:
                book = None
        if book:
            # 若book存在  filter(foo__isnull=False)   exclude(foo=None)
            book.img_cata = book.imgscatalogue_set.all()
            book.article_cata = book.articlecatalogue_set.all()
            book.ztree_cata = book.ztreecatalogue_set.all()
            book.imgdb_title = book.imgsdatabase_set.filter(catalogue_id=None)
            book.article_title = book.article_set.filter(catalogue_id=None)
            book.ztree_title = book.ztree_set.filter(catalogue_id=None)
        return render(request, 'family_create.html', {'book': book})

    def post(self, request, book_id):
        operate = request.POST.get('operate')
        # print(operate)
        if operate == 'save':
            post = request.POST
            file = request.FILES.get('file')    # 谱书封面文件
            user = request.user    # 当前登录的用户
            new_book_id = self.store_book(post, file, user, book_id)
            return JsonResponse({'res': 1, 'successmsg': '数据保存成功', 'new_book_id': new_book_id})
        elif operate == 'delete':
            self.delete_book(book_id)
            return JsonResponse({'res': 1, 'successmsg': '删除成功'})

    def store_book(self, post, file, user, book_id):
        # 保存谱书信息
        # print(post)
        book_id = int(book_id)
        if book_id:
            # 若book_id不为0，则表明是修改谱书内容，需到数据库中查找对应谱书
            try:
                gene_book = GeneBook.objects.get(id=book_id)
            except GeneBook.DoesNotExist:
                return False
            # 判断是否需要更换谱书封面
            if file:
                if gene_book.img_name != post['filename']:
                    fastdfs = FDFSStorage()
                    gene_book.img = fastdfs.save(file.name, file)
                    gene_book.img_name = post['filename']
        else:
            # 若book_id为0，则表明是新创建谱书
            gene_book = GeneBook()
            if file:
                fastdfs = FDFSStorage()
                gene_book.img = fastdfs.save(file.name, file)
                gene_book.img_name = post['filename']
            else:
                gene_book.img_name = None
        gene_book.name = post['bookname']
        gene_book.author = post['author']
        gene_book.desc = post['bookdesc']
        gene_book.province = post['province']
        gene_book.city = post['city']
        gene_book.district = post['district']
        gene_book.addr = post['address']
        gene_book.grant = int(post['grant'])
        gene_book.user_id = user
        gene_book.audit_status = int(post['audit_select'])

        gene_book.save()
        return gene_book.id

    def delete_book(self,book_id):
        try:
            genebook = GeneBook.objects.get(id=book_id)
        except GeneBook.DoesNotExist:
            return JsonResponse({'errmsg': '操作失败'})

        genebook.delete()
        return True

class CatalogueView(LoginRequiredMixin,View):
    def get(self, request):
        type = request.GET.get('type')
        cata_id = request.GET.get('cata_id')
        # print(request.GET)
        if cata_id:
            cata_id = int(cata_id)
            if type == 'img':
                try:
                    catalogue = ImgsCatalogue.objects.get(id=cata_id)
                except ImgsCatalogue.DoesNotExist:
                    return JsonResponse({'res':2, 'errormsg': "数据传输错误"})
                titles = catalogue.imgsdatabase_set.all()
            elif type == 'article':
                try:
                    catalogue = ArticleCatalogue.objects.get(id=cata_id)
                except ArticleCatalogue.DoesNotExist:
                    return JsonResponse({'res':2, 'errormsg': "数据传输错误"})
                titles = catalogue.article_set.all()
            elif type == 'ztree':
                try:
                    catalogue = ZtreeCatalogue.objects.get(id=cata_id)
                except ZtreeCatalogue.DoesNotExist:
                    return JsonResponse({'res':2, 'errormsg': "数据传输错误"})
                titles = catalogue.ztree_set.all()
            else:
                return JsonResponse({'res':2, 'errormsg': "数据传输错误"})
        else:
            return JsonResponse({'res': 2, 'errormsg': "数据传输错误"})

        title_list = []
        if titles:
            for title in titles:
                title_dict = {}
                title_dict['id'] = title.id
                title_dict['name'] = title.name
                title_list.append(title_dict)

        return JsonResponse({'res': 1, 'successmsg': title_list})

    def post(self, request):
        # 处理目录操作
        # print(request.POST)
        operate = request.POST.get('operate')
        post = request.POST
        if operate == 'add':
            res = self.add_catalogue(post)
            if not res:
                return JsonResponse({'res': 3, 'errormsg': '数据添加失败'})
        elif operate == 'edit':
            res = self.edit_catalogue(post)
        elif operate == 'delete':
            res = self.delete_catalogue(post)
        else:
            JsonResponse({'res': 2, 'errormsg': '数据传输有误'})

        return JsonResponse({'res':1, 'successmsg': res})

    def add_catalogue(self,post):
        # 添加目录
        # 获取数据
        # print("add_catalogue")
        type = post['type']
        name = post['title']
        book_id = int(post['book_id'])
        try:
            book = GeneBook.objects.get(id=book_id)
        except GeneBook.DoesNotExist:
            return False
        # 判断添加类型
        if type == 'img':
            catalogue = ImgsCatalogue()
        elif type == 'article':
            catalogue = ArticleCatalogue()
        elif type == 'ztree':
            catalogue = ZtreeCatalogue()
        else:
            return False
        # 数据库操作
        catalogue.name = name
        catalogue.book_id = book
        catalogue.save()
        # 返回目录id
        return catalogue.id

    def edit_catalogue(self, post):
        # 编辑目录
        cata_id = int(post['cata_id'])
        name = post['title']
        type = post['type']
        if type == 'img':
            try:
                catalogue = ImgsCatalogue.objects.get(id=cata_id)
            except ImgsCatalogue.DoesNotExist:
                return False
        elif type == 'article':
            try:
                catalogue = ArticleCatalogue.objects.get(id=cata_id)
            except ArticleCatalogue.DoesNotExist:
                return False
        elif type == 'ztree':
            try:
                catalogue = ZtreeCatalogue.objects.get(id=cata_id)
            except ZtreeCatalogue.DoesNotExist:
                return False
        else:
            return False
        catalogue.name = name
        catalogue.save()
        return '修改成功'

    def delete_catalogue(self, post):
        # 删除目录
        cata_id = int(post['cata_id'])
        type = post['type']
        if type == 'img':
            try:
                catalogue = ImgsCatalogue.objects.get(id=cata_id)
            except ImgsCatalogue.DoesNotExist:
                return False
        elif type == 'article':
            try:
                catalogue = ArticleCatalogue.objects.get(id=cata_id)
            except ArticleCatalogue.DoesNotExist:
                return False
        elif type == 'ztree':
            try:
                catalogue = ZtreeCatalogue.objects.get(id=cata_id)
            except ZtreeCatalogue.DoesNotExist:
                return False
        else:
            return False
        catalogue.delete()

        return '删除成功'

class TitleView(LoginRequiredMixin,View):
    '''目录标题处理'''
    def post(self, request):
        # 处理目录标题操作
        operate = request.POST.get('operate')
        post = request.POST
        if operate == 'add':
            res = self.add_title(post)
            if not res:
                return JsonResponse({'res': 3, 'errormsg': '数据添加失败'})
        elif operate == 'edit':
            res = self.edit_title(post)
        elif operate == 'delete':
            res = self.delete_title(post)
        else:
            JsonResponse({'res': 2, 'errormsg': '数据传输有误'})

        return JsonResponse({'res': 1, 'successmsg': res})

    def add_title(self, post):
        # 获取数据
        type = post['type']
        name = post['title']
        book_id = int(post['book_id'])
        cata_id = post['cata_id']

        # # 判断所传目录id是否为空
        # if not cata_id:
        #     # 目录cata_id为空, 设置catalogue_id = None
        #     catalogue = None
        # else:
        #     # 目录cata_id不为空, 判断目录类型，查找对应目录
        #     cata_id = int(cata_id)
        #     if type == 'img':
        #         try:
        #             catalogue = ImgsCatalogue.objects.get(id=cata_id)
        #         except ImgsCatalogue.DoesNotExist:
        #             return False
        #     elif type == 'article':
        #         try:
        #             catalogue = ArticleCatalogue.objects.get(id=cata_id)
        #         except ArticleCatalogue.DoesNotExist:
        #             return False
        #     elif type == 'ztree':
        #         try:
        #             catalogue = ZtreeCatalogue.objects.get(id=cata_id)
        #         except ZtreeCatalogue.DoesNotExist:
        #             return False
        #     else:
        #         return False

        # #  判断所需添加的标题类型
        # if type == 'img':
        #     title = ImgsDatabase()
        # elif type == 'article':
        #     title = Article()
        # elif type == 'ztree':
        #     title = Ztree()
        # else:
        #     return False
        cata_id = int(cata_id)
        if type == 'img':
            try:
                catalogue = ImgsCatalogue.objects.get(id=cata_id)
            except ImgsCatalogue.DoesNotExist:
                catalogue = None
            title = ImgsDatabase()
        elif type == 'article':
            try:
                catalogue = ArticleCatalogue.objects.get(id=cata_id)
            except ArticleCatalogue.DoesNotExist:
                catalogue = None
            title = Article()
        elif type == 'ztree':
            try:
                catalogue = ZtreeCatalogue.objects.get(id=cata_id)
            except ZtreeCatalogue.DoesNotExist:
                catalogue = None
            title = Ztree()
        else:
            return False


        # 获取获取所属谱书
        try:
            book = GeneBook.objects.get(id=book_id)
        except GeneBook.DoesNotExist:
            return False

        # print(book)

        # 保存数据
        title.name = name
        title.book_id = book
        title.catalogue_id = catalogue
        title.save()
        return  title.id

    def edit_title(self, post):
        article_id = int(post['article_id'])
        name = post['title']
        type = post['type']
        if type == 'img':
            try:
                title = ImgsDatabase.objects.get(id=article_id)
            except ImgsDatabase.DoesNotExist:
                return False
        elif type == 'article':
            try:
                title = Article.objects.get(id=article_id)
            except Article.DoesNotExist:
                return False
        elif type == 'ztree':
            try:
                title = Ztree.objects.get(id=article_id)
            except Ztree.DoesNotExist:
                return False
        else:
            return False
        title.name = name
        title.save()
        return  '修改成功'

    def delete_title(self, post):
        article_id = int(post['article_id'])
        type = post['type']
        print("delete_article")
        if type == 'img':
            try:
                title = ImgsDatabase.objects.get(id=article_id)
            except ImgsDatabase.DoesNotExist:
                return False
        elif type == 'article':
            try:
                title = Article.objects.get(id=article_id)
            except Article.DoesNotExist:
                return False
        elif type == 'ztree':
            try:
                title = Ztree.objects.get(id=article_id)
            except Ztree.DoesNotExist:
                return False
        else:
            return False
        title.delete()

        return '删除成功'
