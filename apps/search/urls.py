from django.conf.urls import url
from search.views import SearchBookView, SearchBookImgView,SearchBookArticleView,SearchBookZtreePersonView,SearchCultureArticleView

urlpatterns = [
    url(r'^book$', SearchBookView.as_view(), name='book'),  # 查询谱书
    url(r'^img$', SearchBookImgView.as_view(), name='img'),  # 查询谱书图片
    url(r'^article$', SearchBookArticleView.as_view(), name='article'),  # 查询谱书谱文
    url(r'^person$', SearchBookZtreePersonView.as_view(), name='person'),  # 查询谱书世系人物
    url(r'^culture_article$', SearchCultureArticleView.as_view(), name='culture_article'),  # 查询谱书
]
