from django.conf.urls import url
from culture.views import CulCenterView, CulReadView
# from family.views import IndexView,ZTreeView

urlpatterns = [
    url(r'^center$', CulCenterView.as_view(), name='center'),  # 文化中心页面
    # url(r'^center/(?P<catagory_id>\d+)$', CulCenterView.as_view(), name='center'),  # 文化中心页面
    url(r'^read/(?P<article_id>\d+)$', CulReadView.as_view(), name='read'),  # 文化中心页面
]
