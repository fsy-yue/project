from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

class LoginRequiredMixin(object):

    @classmethod
    def as_view(cls, **initkwargs):
        # 调用父类的as_view
        view = super(LoginRequiredMixin, cls).as_view(**initkwargs)
        return login_required(view)

class Page():
    def __init__(self,objects, numbers, page):
        self.objects = objects
        self.numbers = numbers
        self.page = page

    def paging(self):
        # 对数据进行分页
        paginator = Paginator(self.objects, self.numbers)

        # 获取第page页的内容
        try:
            page = int(self.page)
        except Exception as e:
            page = 1

        if page > paginator.num_pages:
            page = 1

        # 获取第page页的Page实例对象
        imgs_page = paginator.page(page)

        # todo: 进行页码的控制，页面上最多显示5个页码
        # 1.总页数小于5页，页面上显示所有页码
        # 2.如果当前页是前3页，显示1-5页
        # 3.如果当前页是后3页，显示后5页
        # 4.其他情况，显示当前页的前2页，当前页，当前页的后2页
        num_pages = paginator.num_pages
        if num_pages < 5:
            pages = range(1, num_pages + 1)
        elif page <= 3:
            pages = range(1, 6)
        elif num_pages - page <= 2:
            pages = range(num_pages - 4, num_pages + 1)
        else:
            pages = range(page - 2, page + 3)

        pages_num = paginator.num_pages

        context = {
            'pages': pages,
            'imgs_page': imgs_page,
            'pages_num': pages_num,
        }
        return context


class FooterPage():
    def __init__(self,objects, numbers, page):
        self.objects = objects
        self.numbers = numbers
        self.page = page

    def paging(self):
        # 对数据进行分页
        paginator = Paginator(self.objects, self.numbers)
        imgdb_page = 1
        for imgdb in self.objects:
            if imgdb.id == int(self.page):
                break
            imgdb_page += 1

        if imgdb_page >= 2:
            footer_page_prev = imgdb_page - 1
            imgdb_page_prev = paginator.page(footer_page_prev)
        else:
            imgdb_page_prev = None
        if imgdb_page <= paginator.num_pages - 1:
            footer_page_next = imgdb_page + 1
            imgdb_page_next = paginator.page(footer_page_next)
        else:
            imgdb_page_next = None

        num_pages = paginator.num_pages

        context = (imgdb_page_prev, imgdb_page_next, num_pages,imgdb_page)
        return context


