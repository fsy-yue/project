from django.conf.urls import url
from family.views import IndexView, FamilyCenterView, FamilyCreateView, FamilyReadView, CatalogueView, TitleView

urlpatterns = [
    url(r'^index$', IndexView.as_view(), name="index"),  # 首页

    url(r'^center$', FamilyCenterView.as_view(), name="center"),  # 家谱中心页面
    url(r'^read/(?P<book_id>\d+)$', FamilyReadView.as_view(), name="read"),  # 家谱中心家谱阅读页面
    url(r'^create/(?P<book_id>\d+)$', FamilyCreateView.as_view(), name="create"),  # 家谱中心家谱创建页面

    url(r'^catalogue', CatalogueView.as_view(), name="catalogue"),   # 目录操作
    url(r'^title', TitleView.as_view(), name="title"),  # 标题操作
]
