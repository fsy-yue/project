from django.conf.urls import url
from user.views import RegisterView, ActiveView, LoginView, LogoutView, \
    ForgetPwdView, ChangePwdView, ChangePwdView1, ChangeEmailView, UserInfoView, UserGeneView

urlpatterns = [

    url(r'^register$', RegisterView.as_view(), name='register'), # 注册
    url(r'^active/(?P<token>.*)$', ActiveView.as_view(), name='active'), # 用户激活

    url(r'^login$', LoginView.as_view(), name='login'), # 登录
    url(r'^logout$', LogoutView.as_view(), name='logout'), # 注销登录

    url(r'^forget_pwd$', ForgetPwdView.as_view(), name='forget_pwd'), # 忘记密码
    url(r'^change_pwd/(?P<token>.*)$', ChangePwdView.as_view(), name='change_pwd'), # 忘记密码修改密码

    url(r'^info$', UserInfoView.as_view(), name='user_center_info'),  # 显示用户中心个人信息页面
    url(r'^change_email$', ChangeEmailView.as_view(), name='change_email'), # 修改绑定的邮箱
    url(r'^gene$', UserGeneView.as_view(), name='user_center_gene'),  # 显示用户中心个人家谱页面
]