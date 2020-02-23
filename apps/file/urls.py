from django.conf.urls import url
from file.views import UploadImgView, ShowImgView, UploadArticleView, ShowArticleView, UploadZTreeView, ShowZTreeView

urlpatterns = [
    url(r'^upload_img/(?P<imgdb_id>\d+)$', UploadImgView.as_view(), name="upload_img"),  # 上传图片页面
    url(r'^show_img/(?P<imgdb_id>\d+)$', ShowImgView.as_view(), name="show_img"),  # 预览图片页面
    # url(r'^show_img/(?P<imgdb_id>\d+)/(?P<page>\d+)$', ShowImgView.as_view(), name="show_img"),  # 预览图片页面

    url(r'^upload_file/(?P<article_id>\d+)$', UploadArticleView.as_view(), name="upload_file"),  # 上传文件页面
    url(r'^show_file/(?P<article_id>\d+)$', ShowArticleView.as_view(), name="show_file"),  # 普文页面

    url(r'^upload_ztree/(?P<ztree_id>\d+)$', UploadZTreeView.as_view(), name="upload_ztree"),  # 上传世系表页面
    url(r'^show_ztree/(?P<ztree_id>\d+)$', ShowZTreeView.as_view(), name="show_ztree"),  # 查看世系表页面
]
