from django.shortcuts import render
from django.views.generic import View
from django.http import HttpResponse,JsonResponse

from file.models import Imgs, ImgsDatabase, Files, FilesDatabase,Article, Ztree, ZtreeNode, NodePerson

from utils.fdfs.storage import FDFSStorage
from datetime import datetime
from utils.mixin import LoginRequiredMixin, Page,FooterPage
# Create your views here.

# 图片类处理
class UploadImgView(LoginRequiredMixin,View):
    '''上传图片视图函数'''
    def get(self, request, imgdb_id):
        '''展示上传图片页面'''
        try:
            imgdb = ImgsDatabase.objects.get(id=imgdb_id)
        except ImgsDatabase.DoesNotExist:
            return HttpResponse("获取失败")
        book_id = imgdb.book_id.id

        imgs = imgdb.imgs_set.all().order_by('-create_time')

        page = request.GET.get('page')
        pageobj = Page(imgs, 12, page)
        context = pageobj.paging()
        context['imgs'] = imgs
        context['imgdb_id'] = imgdb_id
        context['imgdb'] = imgdb
        context['book_id'] = book_id

        return  render(request, 'family_create_upload_img.html',context)

    def post(self, request, imgdb_id):
        operate = request.POST.get('operate')
        if operate == 'save':
            imgs = request.FILES.getlist('files')
            details = request.POST.getlist('details')
            if len(imgs)==0:
                return JsonResponse({'res': 2,'errmsg': '当前数据为空，请重新选择数据上传'})
            res = self.save_img(imgs,details,imgdb_id)
        elif operate == 'edit':
            img_id = request.POST.get('img_id')
            detail = request.POST.get('detail')
            try:
                img = Imgs.objects.get(id=img_id)
            except Imgs.DoesNotExist:
                return JsonResponse({'res': 3, 'errmsg': '数据错误，请重试'})
            img.detail = detail
            img.save()
            res = '修改成功'
            # post = request.POST
            # res = self.edit_img(self,post)
            # if res[0]:
            #     res = res[1]
        elif operate == 'delete':
            img_id = request.POST.get('img_id')
            try:
                img = Imgs.objects.get(id=img_id)
            except Imgs.DoesNotExist:
                return JsonResponse({'res': 4, 'errmsg': '数据错误，请重试'})
            img.delete()
            res = '删除成功'
            # post = request.POST
            # res = self.delete_img(self, post)
            # if res[0]:
            #     res = res[1]
        else:
            return JsonResponse({'res': 3,'errmsg': '操作有误，请重试'})

        return JsonResponse({'res':1, 'successmsg':res})

    def save_img(self,imgs,details, imgdb_id):
        try:
            img_database = ImgsDatabase.objects.get(id=imgdb_id)
        except ImgsDatabase.DoesNotExist:
            return False

        # 将图片保存到fastdfs存储系统中
        fastdfs = FDFSStorage()
        id_list = []  # 记录所添加图片的id用于传递到前端
        for i in range(len(imgs)):
            img = Imgs()
            # 将图片保存到fastdfs存储系统中
            img.img = fastdfs.save(imgs[i].name, imgs[i])
            img.name = imgs[i].name
            img.detail = details[i]
            img.imgsdb_id = img_database
            img.save()
            id_list.append(img.id)
        res = '上传成功', id_list
        return res

    def edit_img(self, post):
        img_id = post['img_id']
        detail = post['detail']
        try:
            img = Imgs.objects.get(id=img_id)
        except Imgs.DoesNotExist:
            return (0, '数据错误，请重试')
        img.detail = detail
        img.save()

        return (1,'修改成功')

    def delete_img(self, post):
        img_id = post['img_id']
        try:
            img = Imgs.objects.get(id=img_id)
        except Imgs.DoesNotExist:
            return (0, '数据错误，请重试')
        img.delete()
        return (1,'删除成功')

class ShowImgView(LoginRequiredMixin,View):
    '''展示图片视图类'''
    def get(self, request,imgdb_id):
        '''展示图片'''
        # 获取图片信息
        try:
            imgdb = ImgsDatabase.objects.get(id=imgdb_id)
        except ImgsDatabase.DoesNotExist:
            return HttpResponse("获取失败")
        book = imgdb.book_id


        imgdbs = ImgsDatabase.objects.filter(book_id=book)
        paginator = FooterPage(imgdbs, 1, imgdb_id)
        imgdb_page_prev, imgdb_page_next,num_pages,imgdb_page = paginator.paging()

        imgs = imgdb.imgs_set.all().order_by('-create_time')
        page = request.GET.get('page')
        pageobj = Page(imgs, 12, page)
        context = pageobj.paging()

        context['imgdb_id'] = imgdb_id
        context['imgdb'] = imgdb
        context['book'] = book
        context['imgdb_page_prev'] = imgdb_page_prev
        context['imgdb_page_next'] = imgdb_page_next

        img_id = request.GET.get('img_id')
        if img_id:
            paginator = FooterPage(imgs, 1, img_id)
            img_page_prev, img_page_next,num_pages,img_page= paginator.paging()
            img = Imgs.objects.get(id=img_id)
            context['img'] = img
            context['img_page'] = img_page
            context['img_page_prev'] = img_page_prev
            context['img_page_next'] = img_page_next
            context['num_pages'] = num_pages


        return render(request, 'family_read_preview_img.html', context)

# 谱文类处理
class UploadArticleView(LoginRequiredMixin,View):
    '''上传文件视图类'''

    def get(self, request, article_id):
        '''上传文件页面'''
        try:
            article = Article.objects.get(id=article_id)
        except Article.DoesNotExist:
            return HttpResponse("获取失败")
        book_id = article.book_id.id
        context = {
            'article': article,
            'article_id': article_id,
            'book_id': book_id,
        }
        # print(article.content)

        return render(request, 'family_create_upload_file.html',context)

    def post(self, request, article_id):
        '''上传文件处理函数'''
        article_content = request.POST.get('article_content')

        if article_content == '':
            return JsonResponse({'errmsg': '请添加谱文内容'})

        try:
            article = Article.objects.get(id=article_id)
        except Article.DoesNotExist:
            return HttpResponse("获取失败")

        # article.name = article_title
        article.content = article_content
        article.save()

        return JsonResponse({'res':1, 'successmsg': '谱文保存成功'})

class ShowArticleView(LoginRequiredMixin,View):
    '''展示谱文'''
    def get(self, request, article_id):
        '''普文预览页面'''
        # 获取文件信息
        try:
            article = Article.objects.get(id=article_id)
        except Article.DoesNotExist:
            return HttpResponse("获取失败")

        book = article.book_id

        articles = Article.objects.filter(book_id=book)

        paginator = FooterPage(articles, 1, article_id)
        imgdb_page_prev, imgdb_page_next, num_pages,imgdb_page = paginator.paging()


        context = {
            'article': article,
            'article_id': article_id,
            'book': book,
            'imgdb_page_prev': imgdb_page_prev,
            'imgdb_page_next': imgdb_page_next
        }

        return render(request, 'family_read_preview_article.html', context)

# 世系表类处理
class UploadZTreeView(LoginRequiredMixin,View):
    '''ZTree测试'''
    def get(self, request,ztree_id):
        '''ZTree页面'''
        # 获取ztree树
        try:
            ztree = Ztree.objects.get(id=ztree_id)
        except Ztree.DoesNotExist:
            ztree = None

        if(request.GET.get('_')):
            if ztree:
                ztree_set = ztree.ztreenode_set.all()
                ztree_list = []
                for ztreeNode in ztree_set:
                    ztree_dict = self.get_data(ztreeNode)
                    ztree_list.append(ztree_dict)

                zNodes = ztree_list
                zNodes_len = len(zNodes)
                if not zNodes_len:
                    return JsonResponse({"res": 2})
                return JsonResponse({"res": 1, "data": zNodes})
        else:
            book_id = ztree.book_id.id
            context = {'ztree': ztree, 'ztree_id': ztree_id, 'book_id': book_id}
            return render(request, 'family_create_upload_genetree.html', context)

    def post(self, request,ztree_id):
        '''加载数据'''
        try:
            ztree = Ztree.objects.get(id=ztree_id)   # 获取ztree树
        except Ztree.DoesNotExist:
            ztree = None

        if not ztree:
            return JsonResponse({"res": 5, "errmsg": '查无所获'})

        # 获取数据
        id = int(request.POST.get('id'))
        operate = request.POST.get('operate')
        post = request.POST

        if id:   # 若有id，则到数据库中查询id所对应的节点信息
            # 验证数据
            try:
                ztreeNode = ztree.ztreenode_set.get(id=id)   # 获取ztree树节点
            except ZtreeNode.DoesNotExist:
                ztreeNode = None
            if not ztreeNode:
                return JsonResponse({"res": 2, "errmsg": "数据库中无此人的相关信息"})

            if operate == 'delete':
                res = self.delete_node(ztreeNode)
            elif operate == 'add':
                res = self.add_node(ztreeNode,ztree,post)
            elif operate == 'edit':
                res = self.edit_node(ztreeNode, post)
            else:
                return JsonResponse({"res": 3, "errmsg": "操作失败，请重新开始"})
        elif operate == 'add':              # 若无id且对应的操作为add，则表明是添加根节点
            res = self.add_node(None,ztree,post)
        else:
            return JsonResponse({"res": 4, "errmsg": "操作失败，请重新开始"})
        return JsonResponse({"res": 1, "successmsg": res})

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
            return  False

        if node_person.sex:
            node_info['sex'] = 1
        else:
            node_info['sex'] = 0
        if node_person.birthdate:
            node_info['birthday'] = str(node_person.birthdate)
        else:
            node_info['birthday'] = ''
        if node_person.birthdate:
            node_info['deathday'] = str(node_person.deathdate)
        else:
            node_info['deathday'] = ''
        node_info['lastname'] = node_person.last_name
        node_info['firstname'] = node_person.first_name
        node_info['othername'] = node_person.other_name
        node_info['seniority'] = node_person.seniority
        node_info['sex'] = node_person.sex
        node_info['spouse'] = node_person.spouse
        node_info['desc'] = node_person.desc

        return node_info

    def set_data(self, ztreenode, post):
        '''整理数据信息'''
        node_person = NodePerson()

        if isinstance(ztreenode, ZtreeNode):
            # 若传入的是ZtreeNode类型，则表示为设置新建子节点对应的人物信息，需要新建NodePerson对象并添加node_id
            node_person = NodePerson()
            node_person.node_id = ztreenode
        elif isinstance(ztreenode, NodePerson):
            # 若传入的是NodePerson类型，则表示为编辑已有节点对应的人物信息,只需要赋值即可
            node_person = ztreenode
        else:
            return  False

        if post['birthday']:
            node_person.birthdate = datetime.strptime(post['birthday'], '%Y-%m-%d')
        else:
            node_person.birthdate = None
        if post['deathday']:
            node_person.deathdate = datetime.strptime(post['deathday'], '%Y-%m-%d')
        else:
            node_person.deathdate = None
        node_person.last_name = post['lastname']
        node_person.first_name = post['firstname']
        node_person.other_name = post['othername']
        node_person.seniority = int(post['seniority'])
        node_person.sex = int(post['sex'])
        print(node_person.sex)
        node_person.spouse = post['spouse']
        node_person.desc = post['desc']
        node_person.save()

        node_person.node_id.name = node_person.last_name+node_person.first_name
        node_person.node_id.save()

        # person_info = self.get_data(node_person)
        # return person_info
        return node_person

    def add_node(self,ztreenode, ztree, post):
        '''添加节点'''
        # 创建世系表节点
        son_ztreenode = ZtreeNode()
        if not ztreenode:    #  若传入的节点为空，则设置新建节点的父亲节点为空
            son_ztreenode.pid = None
            pid = 0
        else:           #  若传入的节点不为空，则设置新建节点的父亲节点为传入的新节点
            son_ztreenode.pid = ztreenode
            pid = ztreenode.id
        son_ztreenode.name = post['name']
        son_ztreenode.ztree_id = ztree
        son_ztreenode.save()

        # 设置新建节点对应的人物信息
        # person_info = self.set_data(son_ztreenode, post)
        son_node = self.set_data(son_ztreenode, post)
        person_info = self.get_data(son_node)

        if person_info:  # 设置成功，分别获取对应节点的id，pid，name，用于ztree使用
            person_info['id'] = son_ztreenode.id
            person_info['pid'] = pid
            person_info['name'] = son_ztreenode.name
            res = ("人物信息添加成功", person_info)
        else:     # 设置不成功，则将新建的节点删除，以免出现与节点人物信息表不能一一对应的情况
            ztree.ztreenode_set.get(id=son_ztreenode.id).delete()
            res = ("人物信息添加失败")

        return  res

    def edit_node(self, ztreenode, post):
        '''编辑节点信息'''
        node_person = ztreenode.nodeperson

        # person_info = self.set_data(node_person, post)
        node = self.set_data(node_person, post)
        person_info = self.get_data(node)

        if person_info:
            person_info['name'] = post['name']
            person_info['id'] = post['id']
            res = ("人物信息修改成功", person_info)
        else:
            res = ("人物信息修改失败")

        return res

    def delete_node(self, ztreenode):
        '''递归删除节点，及其后代'''
        if ztreenode:
            # 假删除
            ztreenode.is_delete = True  # 标记人物已被删除
            ztreenode.save()
            # 真删除
            # node_person = ztreenode.nodeperson  # 获取ztreenode对应的人物信息
            # node_person.delete()
            # ztreenode.delete()
        # 查询节点是否有后代
        ztree_node_sons = ZtreeNode.objects.filter(pid=ztreenode.id)

        if not ztree_node_sons:
            return "人物信息删除成功"
        else:
            for ztree_node in ztree_node_sons:
                self.delete_node(ztree_node)

class ShowZTreeView(LoginRequiredMixin,View):
    '''ZTree测试'''
    def get(self, request,ztree_id):
        '''ZTree页面'''

        try:
            ztree = Ztree.objects.get(id=ztree_id)   # 获取ztree树
        except Ztree.DoesNotExist:
            ztree = None

        book = ztree.book_id

        if (request.GET.get('_')):
            ztreenode_set = ztree.ztreenode_set.all()
            ztreenode_list = []
            for ztreenode in ztreenode_set:

                ztreenode_dict = self.get_data(ztreenode)
                ztreenode_list.append(ztreenode_dict)

            zNodes = ztreenode_list
            zNodes_len = len(zNodes)
            if not zNodes_len:
                return JsonResponse({"res": 2})

            return JsonResponse({"res": 1, "data": zNodes})
        else:
            ztrees = Ztree.objects.filter(book_id=book)
            paginator = FooterPage(ztrees, 1, ztree_id)
            imgdb_page_prev, imgdb_page_next,num_pages,imgdb_page = paginator.paging()

            node_id = request.GET.get('node_id')
            node_rank = request.GET.get('node_rank')
            context = {
                'ztree': ztree,
                'ztree_id': ztree_id,
                'book': book,
                'imgdb_page_prev': imgdb_page_prev,
                'imgdb_page_next': imgdb_page_next,
                'node_id': node_id,
                'node_rank': node_rank,
            }
            return render(request, 'family_read_preview_genetree.html',context)

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



# 预留版块
class UploadFileView(View):
    '''上传文件视图类'''

    def get(self, request, article_id):
        '''上传文件页面'''
        return render(request, 'family_create_upload_file.html', {'article_id': article_id})

    def post(self, request, article_id):
        '''上传文件处理函数'''
        article_title = request.POST.get('article_title')
        article_content = request.POST.get('article_content')

        if article_title == '':
            return JsonResponse({'errmsg': '请添加谱文标题'})
        elif article_content == '':
            return JsonResponse({'errmsg': '请添加谱文内容'})

        article = Article()
        article.name = article_title
        article.content = article_content
        article.save()

        # file = Files()
        # file.name = article_title
        # file.content = article_content
        # file.save()

        return JsonResponse({'errmsg': '谱文上传成功'})

class ShowFileView(View):
    '''展示谱文'''

    def get(self, request, article_id):
        '''普文预览页面'''
        # 获取文件信息
        files = Files.objects.all().order_by('id')
        articles_num = len(files)
        context = {
            'articles_num': articles_num,
            'files': files,
            'article_id': article_id
        }
        return render(request, 'family_read_preview_article.html', context)



