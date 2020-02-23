from django.shortcuts import render
from django.http import JsonResponse
from django.views.generic import View

from utils.mixin import Page,FooterPage

from family.models import GeneBook, ImgsCatalogue, ArticleCatalogue, ZtreeCatalogue
from file.models import Imgs, ImgsDatabase,Article, Ztree, ZtreeNode, NodePerson
from culture.models import CultureCategory,CultureArticle

from django.db.models import Q

import re


class SearchBookView(View):
    def get(self, request):
        '''查询谱书'''
        search_key = request.GET.get('q')

        books = GeneBook.objects.filter(Q(name__contains=search_key)|Q(author__contains=search_key)|Q(addr__contains=search_key))

        book_list = []
        for book in books:
            if book.audit_status != 3:
                continue
            if book.grant:
                continue
            book_list.append(book)

        books = book_list

        page = request.GET.get('page')
        pageobj = Page(books, 8, page)
        context = pageobj.paging()
        context['query'] = search_key


        if books:
            context['books_total_num'] = len(books)
        else:
            context['books_total_num'] = 0

        return render(request,'search_book.html', context)

class SearchBookImgView(View):
    def get(self, request):
        '''查询谱书图片'''
        search_key = request.GET.get('q')
        imgs = Imgs.objects.filter(Q(detail__contains=search_key))

        img_list = []
        for img in imgs:
            if img.imgsdb_id.book_id.audit_status != 3:
                continue
            if img.imgsdb_id.book_id.grant:
                continue
            img_list.append(img)
        imgs = img_list

        page = request.GET.get('page')
        pageobj = Page(imgs, 12, page)
        context = pageobj.paging()

        # 左右箭头换图
        img_id = request.GET.get('img_id')
        if img_id:
            if imgs:
                paginator = FooterPage(imgs, 1, img_id)
                img_page_prev, img_page_next, num_pages, img_page = paginator.paging()
                img = Imgs.objects.get(id=img_id)
                print(img)
                context['img'] = img
                context['img_page'] = img_page
                context['img_page_prev'] = img_page_prev
                context['img_page_next'] = img_page_next
                context['num_pages'] = num_pages

        context['query'] = search_key
        if imgs:
            context['imgs_total_num'] = len(imgs)
        else:
            context['imgs_total_num'] = 0
        return render(request, 'search_book_img.html', context)

class SearchBookArticleView(View):
    def get(self, request):
        '''查询谱书图片'''
        search_key = request.GET.get('q')
        articles = Article.objects.filter(Q(name__contains=search_key)|Q(content__contains=search_key))

        article_list = []
        for article in articles:
            if article.book_id.audit_status != 3:
                continue
            if article.book_id.grant:
                continue
            article_list.append(article)
            article.desc = self.handle_str(article.content[:1000])
        articles = article_list

        page = request.GET.get('page')
        pageobj = Page(articles, 5, page)
        context = pageobj.paging()

        context['query'] = search_key
        if articles:
            context['articles_total_num'] = len(articles)
        else:
            context['articles_total_num'] = 0

        return render(request, 'search_book_article.html', context)

    def handle_str(self, str):
        '''截取文章字符串'''
        # 1.获取双字节字符列表
        str_list = re.findall('[^x00-xff]', str)
        # 2.将双字节字符连成字符串
        str1 = ''
        for a in str_list:
            str1 += a
        # 3.获取双字节中的汉字，字母，数字，下划线的的列表
        str_list = re.findall('[a-zA-Z0-9_\u4e00-\u9fa5]+', str1)

        # 4.删除所获列表中的y，z，“新宋体”等字符（串）
        str2 = []
        for a in str_list:
            if a == 'y':
                continue
            if a == 'z':
                continue
            if a == '新宋体':
                continue
            str2.append(a)

        # 5.将最终获得的所有字符用‘，’拼接
        res = ','.join(str2)

        return  res


class SearchBookZtreePersonView(View):

    def __init__(self):
        self.node_list = []

    def get(self, request):
        '''查询谱书世系人物'''
        search_key = request.GET.get('q')

        key = search_key.lstrip('王')

        # 判断是哪个页面发起的访问：世系表页面where，需要世系节点id，
        where = request.GET.get('where')
        if where == 'ztree':
            # 若是世系表阅读发起的异步请求
            ztree_id = request.GET.get('id')
            try:
                ztree = Ztree.objects.get(id=ztree_id)
            except:
                return JsonResponse({"res": 2, "errmsg": '世系表获取失败'})
            persons = NodePerson.objects.filter(first_name=key)

            if not persons:
                return JsonResponse({"res": 3, "errmsg": '无相关人物信息'})

            person_list = []
            person_dict = {}
            for person in persons:
                if person.node_id.ztree_id == ztree:
                    person = self.manage_info(person)
                    person_dict['name'] = search_key
                    person_dict['rank'] = person.rank
                    person_dict['brank'] = person.brank
                    person_dict['ztree'] = person.node_id.ztree_id.name
                    person_dict['node_id'] = person.node_id.id
                    if person.node_id.pid:
                        person_dict['parent'] = person.node_id.pid.name
                    else:
                        person_dict['parent'] = '根节点人物'
                        person_dict['brank'] = ''
                    person_list.append(person_dict)
            return JsonResponse({"res": 1, "successmsg": person_list})

        persons = NodePerson.objects.filter(
            Q(first_name__contains=key) | Q(other_name__contains=key) | Q(desc__contains=key))

        person_list = []
        for person in persons:
            if person.node_id.ztree_id.book_id.audit_status != 3:
                continue
            if person.node_id.ztree_id.book_id.grant:
                continue
            person_list.append(self.manage_info(person))

        persons = person_list

        page = request.GET.get('page')
        pageobj = Page(persons, 5, page)
        context = pageobj.paging()

        context['query'] = search_key
        if persons:
            context['persons_total_num'] = len(persons)
        else:
            context['persons_total_num'] = 0

        return render(request, 'search_book_person.html', context)

    def post(self, request):
        # 1.获取节点id
        node_id = request.POST.get('node_id')

        # 2.查询节点信息
        ztreenode = ZtreeNode.objects.get(id=node_id)

        self.node_list.append(ztreenode)
        self.node_ergodic(ztreenode)
        print(self.node_list)
        ztreenode_list = []
        for ztreenode in self.node_list:
            ztreenode_dict = self.get_data(ztreenode)
            ztreenode_list.append(ztreenode_dict)
        zNodes = ztreenode_list
        print(zNodes)

        # return JsonResponse({"res": 1, "data": zNodes})

        return JsonResponse({"res": 1, "successmsg": zNodes})

    def node_ergodic(self, ztreenode):
        '''递归查询子节点'''
        # 获取传入节点的子节点
        ztreenode_sons = ZtreeNode.objects.filter(pid=ztreenode)

        # 若其含有子节点，遍历子节点
        if ztreenode_sons:
            self.node_list.extend(ztreenode_sons)
            for ztreenode_son in ztreenode_sons:
                # 查询每一个子节点的后代节点
                self.node_ergodic(ztreenode_son)
        else:
            # 若其没有子节点，则返回
            return

    def get_data(self, ztreenode):
        '''整理数据信息'''
        node_info = {}
        if isinstance(ztreenode, ZtreeNode):
            node_person = ztreenode.nodeperson  # 母表对象.子表名小写
            node_info['id'] = ztreenode.id
            node_info['name'] = ztreenode.name
            parent = ztreenode.pid
            if parent:
                node_info['pid'] = parent.id
            else:
                node_info['pid'] = 0
        elif isinstance(ztreenode, NodePerson):
            node_person = ztreenode
        else:
            return False

        node_info['lastname'] = node_person.last_name
        node_info['firstname'] = node_person.first_name
        node_info['othername'] = node_person.other_name
        node_info['seniority'] = node_person.seniority
        node_info['sex'] = node_person.sex
        node_info['spouse'] = node_person.spouse
        if node_person.birthdate:
            node_info['birthday'] = str(node_person.birthdate)
        else:
            node_info['birthday'] = ''
        if node_person.birthdate:
            node_info['deathday'] = str(node_person.deathdate)
        else:
            node_info['deathday'] = ''
        node_info['desc'] = node_person.desc

        return node_info

    def manage_info(self, person):
        '''组织世系人物信息'''

        # 1.计算人物第几世
        i = 1
        p = person.node_id
        while p.pid:
            i += 1
            p = p.pid

        person.rank = i

        # 2.判断人物排行
        seniority = ['独生子', '独生女', '第一', '第二', '第三', '第四', '第五',
                     '第六', '第七', '第八', '第九', '第十', '第十一', '第十二']
        if person.seniority > 2:
            person.brank = '排行' + seniority[person.seniority-1]
        elif person.seniority == 1:
            person.brank = '家中独子'
        else :
            person.brank = '家中独女'

        return person

class SearchCultureArticleView(View):
    def get(self, request):
        '''查询文化中心文章'''
        search_key = request.GET.get('q')
        if search_key:
            articles = CultureArticle.objects.filter(Q(title__contains=search_key)|Q(author__contains=search_key)|Q(introduce__contains=search_key))

            page = request.GET.get('page')
            pageobj = Page(articles, 5, page)
            context = pageobj.paging()
            context['query'] = search_key
        else:
            context = {'query','关键字为空，请重新输入'}

        return render(request,'search_culture_center.html', context)

