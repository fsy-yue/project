from django.shortcuts import render
from django.views.generic import View

from culture.models import CultureCategory,CultureArticle
from utils.mixin import Page,FooterPage

# Create your views here.

class CulCenterView(View):
    '''文化中心视图类'''
    def get(self, request):

        category_id = request.GET.get('select')

        if category_id:
            try:
                category = CultureCategory.objects.get(id=category_id)
            except CultureCategory.DoesNotExist:
                return render(request, 'culture_center.html')
            articles = category.culturearticle_set.all().order_by('-create_time')
            select = category.id
        else:
            articles = CultureArticle.objects.all().order_by('-create_time')
            select = 0

        categorys = CultureCategory.objects.all().order_by('-create_time')

        page = request.GET.get('page')
        pageobj = Page(articles, 5, page)
        context = pageobj.paging()
        # context['category_id'] = category
        context['categorys'] = categorys
        context['select'] = select

        return render(request, 'culture_center.html', context)

class CulReadView(View):
    '''文化中心视图类'''
    def get(self, request, article_id):
        try:
            article = CultureArticle.objects.get(id=article_id)
            article.read_count += 1    # 更新文章阅读量
            article.save()
        except CultureCategory.DoesNotExist:
            return render(request, 'culture_center.html')

        imgdbs = CultureArticle.objects.filter(category_id=article.category_id)
        paginator = FooterPage(imgdbs, 1, article_id)
        imgdb_page_prev, imgdb_page_next,num_pages,imgdb_page= paginator.paging()

        hotarticles = CultureArticle.objects.filter().order_by('-read_count')[:5]

        context = {
            'article': article,
            'article_id': article_id,
            'hotarticles': hotarticles,
            'imgdb_page_prev': imgdb_page_prev,
            'imgdb_page_next': imgdb_page_next
        }

        return render(request, 'culture_read.html',context)