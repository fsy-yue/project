from django.shortcuts import render,redirect
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate, login, logout
from django.views.generic import View
from django.http import HttpResponse,JsonResponse
from django.conf import settings

from user.models import User
from django.core.mail import send_mail  # 发送邮件
from django.conf import settings  # 引入秘钥

from celery_tasks.tasks import send_change_pwd_email
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from itsdangerous import SignatureExpired
from utils.mixin import LoginRequiredMixin,Page
from utils.fdfs.storage import FDFSStorage
import re
# Create your views here.


# /user/register
class RegisterView(View):
    '''注册'''
    def get(self, request):
        '''显示注册页面'''
        return render(request, 'register.html')

    def post(self, request):
        '''进行注册处理'''
        # 接收数据
        username = request.POST.get('username').strip()
        password = request.POST.get('pwd').strip()
        email = request.POST.get('email').strip()

        # 进行数据校验
        if not all([username, password, email]):
            # 数据不完整
            return render(request, 'register.html', {'errmsg': '数据不完整'})

        # 校验邮箱
        if not re.match(r'^[a-z0-9][\w.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$', email):
            return render(request, 'register.html', {'errmsg': '邮箱格式不正确'})

        # 校验用户名是否已被注册
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            # 用户名不存在
            user = None
        if user:
            # 用户名已存在
            return render(request, 'register.html', {'errmsg': '用户名已存在'})

        # 校验邮箱是否被绑定
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            # 邮箱不存在
            user = None
        if user:
            # 邮箱已经被绑定
            return render(request, 'register.html', {'errmsg': '该邮箱已经被绑定'})

        # 进行业务处理: 进行用户注册
        user = User.objects.create_user(username, email, password)
        user.is_active = 1
        user.save()

        # # 发送激活邮件，包含激活链接: http://127.0.0.1:8000/user/active/3
        # # 激活链接中需要包含用户的身份信息, 并且要把身份信息进行加密
        #
        # # 加密用户的身份信息，生成激活token
        # serializer = Serializer(settings.SECRET_KEY, 3600)
        # info = {'confirm':user.id}
        # token = serializer.dumps(info) # bytes
        # token = token.decode()
        #
        # # 发邮件
        # send_register_active_email.delay(email, username, token)

        # 返回应答
        # return render(request, 'register.html', {'errmsg': '请到您注册的邮箱中点击链接，激活账号'})
        return redirect(reverse('user:login'))

class ActiveView(View):
    '''用户激活'''
    def get(self, request, token):
        '''进行用户激活'''
        # 进行解密，获取要激活的用户信息
        serializer = Serializer(settings.SECRET_KEY, 3600)
        try:
            info = serializer.loads(token)
            # 获取待激活用户的id
            user_id = info['confirm']

            # 根据id获取用户信息
            user = User.objects.get(id=user_id)
            user.is_active = 1
            user.save()

            # 跳转到登录页面
            return redirect(reverse('user:login'))
        except SignatureExpired as e:
            # 激活链接已过期
            return HttpResponse('激活链接已过期')

# /user/login
class LoginView(View):
    '''登录'''
    def get(self, request):
        '''显示登录页面'''
        # 获取COOKIES信息

        # 判断是否记住了邮箱
        if 'email' in request.COOKIES:
            username = request.COOKIES.get('email')
        # 判断是否记住了用户名
        elif 'username' in request.COOKIES:
            username = request.COOKIES.get('username')
        else:
            username = ''

        # 判断是否记住了密码
        if 'password' in request.COOKIES:
            password = request.COOKIES.get('password')
            checked = 'checked'
        else:
            password = ''
            checked = ''

        # 组织模板上下文
        context = {
            'username': username,
            'password': password,
            'checked': checked
        }

        # print(context)

        # 使用模板
        return render(request, 'login.html', context)

    def post(self, request):
        '''登录校验'''
        # 接收数据
        username = request.POST.get('username').strip()
        password = request.POST.get('pwd').strip()
        email = ''

        # 校验数据
        if username == '':
            return render(request, 'login.html', {'errmsg': '请填写用户名', 'username': username})
        if password == '':
            return render(request, 'login.html', {'errmsg':'请填写密码', 'username': username})
            # return redirect(reverse('user:login'))

        # 尝试用户输入的是否为邮箱
        if re.match(r'^[a-z0-9][\w.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$', username):
            try:
                user = User.objects.get(email=username)    # 查询数据库，验证用户是否存在
            except User.DoesNotExist:
                return render(request, 'login.html', {'errmsg': '邮箱不存在', 'username': username})
            # 用户存在，分别记录其用户名和邮箱
            username = user.username
            email = user.email

        # 业务处理:登录校验
        user = authenticate(username=username, password=password)
        print(user)
        print(username)
        if user is not None:
            # 用户名密码正确
            if user.is_active:
                # 用户已激活
                # 记录用户的登录状态
                login(request, user)

                # 获取登录后所要跳转到的地址
                # 默认跳转到首页
                next_url = request.GET.get('next', reverse('family:index'))

                # 跳转到next_url
                response = redirect(next_url) # HttpResponseRedirect

                # 判断是否需要记住邮箱
                if email:
                    response.set_cookie('email', email, max_age=7 * 24 * 3600)

                # 记住用户名，并判断是否需要记住密码
                response.set_cookie('username', username, max_age=7 * 24 * 3600)
                remember = request.POST.get('remember')
                if remember == 'on':
                    # 记住密码
                    response.set_cookie('password', password, max_age=7*24*3600)
                else:
                    response.delete_cookie('password')

                # 返回response
                return response
            else:
                # 用户未激活
                return render(request, 'login.html', {'errmsg':'账户未激活'})
        else:
            # 用户名或密码错误
            try:
                user = User.objects.get(username=username)  # 查询数据库，验证用户是否存在
            except User.DoesNotExist:
                return render(request, 'login.html', {'errmsg': '用户名不存在', 'username': username})
            # 用户名无错误，则表明是密码错误
            return render(request, 'login.html', {'errmsg':'密码错误', 'username': username})

# /user/logout
class LogoutView(View):
    '''退出登录'''
    def get(self, request):
        '''退出登录'''
        # 清除用户的session信息
        logout(request)

        # 跳转到首页
        return redirect(reverse('family:index'))

class ForgetPwdView(View):
    '''忘记密码'''
    def get(self, request):
        '''忘记密码页面显示'''
        return render(request, 'forget_pwd.html')
    def post(self, request):
        '''忘记密码处理'''
        # 1.获取数据
        email = request.POST.get('email').strip()

        # 2.验证数据
        # 校验邮箱
        if not re.match(r'^[a-z0-9][\w.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$', email):
            return render(request, 'forget_pwd.html', {'errmsg': '邮箱格式不正确'})

        # 校验邮箱是否被绑定
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            # 邮箱尚未被绑定
            return render(request, 'forget_pwd.html', {'errmsg': '数据库中无该邮箱，请检查您输入的邮箱是否正确'})

        # 3.业务处理
        # 发送修改密码邮件，包含修改密码页面链接: http://192.168.233.142:8000/user/change_pwd/3
        # 链接中需要包含用户的身份信息, 并且要把身份信息进行加密

        # 加密用户的身份信息，生成激活token
        serializer = Serializer(settings.SECRET_KEY, 3600)
        info = {'confirm': user.id}
        token = serializer.dumps(info)  # bytes
        token = token.decode()

        print(email)

        # 发邮件
        send_change_pwd_email.delay(email, user.username, token)
        # subject = '王氏家谱修改密码页面'
        # message = ''
        # sender = settings.EMAIL_FROM
        # receiver = [email]
        # html_message = '<h1>王氏家谱管理与查询系统</h1><h2>%s, 你好！</h2>请点击下面链接跳转到修改密码页面<br/>' \
        #                '<a href="http://120.78.188.2:8000/user/change_pwd/%s">' \
        #                'http://120.78.188.2:8000/user/change_pwd/%s</a>' % (user.username, token, token)
        # send_mail(subject, message, sender, receiver, html_message=html_message)

        # 4.返回应答
        return render(request, 'forget_pwd.html', {'errmsg': '修改密码页面链接已发送到您的邮箱，请到您的邮箱中查证','email':email})

class ChangePwdView(View):
    '''忘记密码修改密码'''
    def get(self, request, token):
        '''修改密码页面显示'''
        return render(request, 'change_pwd.html')

    def post(self, request, token):
        '''修改密码处理'''

        # 进行解密，获取要修改密码的用户信息
        serializer = Serializer(settings.SECRET_KEY, 3600)
        try:
            info = serializer.loads(token)
            # 获取待激活用户的id
            user_id = info['confirm']
            # 根据id获取用户信息
            user = User.objects.get(id=user_id)
        except SignatureExpired as e:
            # 修改密码链接已过期
            return HttpResponse('链接已过期')

        # 业务处理：修改用户密码并保存到数据库
        password = request.POST.get('new_pwd')
        user.set_password(password)
        user.save()

        # 跳转到登录页面
        return redirect(reverse('user:login'))

class UserInfoView(LoginRequiredMixin, View):
    '''用户中心个人信息页'''

    def get(self, request):

        return render(request, 'user_center_info.html')

    def post(self, request):
        # 获取数据
        type = request.POST.get('type')
        post = request.POST
        user = request.user

        # 判断修改类型
        if type == 'info':
            file = request.FILES.get('file')
            res = self.change_info(post,file,user)
        elif type == 'pwd':
            res = self.change_pwd(post, user)
            if not res:
                return JsonResponse({'res': 2, 'errmsg': '原始密码输入不正确'})
        elif type == 'email':
            res = self.change_email(post,user)
            if not res[0]:
                return JsonResponse({'res': 3, 'errmsg': res[1]})
            else:
                res = res[1]

        return JsonResponse({'res': 1, 'successmsg': res})

    def change_info(self, post, file,user):
        print('change_info')
        if file:
            fastdfs = FDFSStorage()
            user.img_url = fastdfs.save(file.name, file)
        if post['usersex']:
            user.sex = int(post['usersex'])
        user.username = post['username']
        user.tele = post['telephone']
        user.addr = post['address']
        user.desc = post['userdesc']
        user.save()
        return '信息修改成功'

    def change_pwd(self, post, user):
        print('change_pwd')
        old_pwd = post['old_pwd']
        new_pwd = post['new_pwd']

        if user.check_password(old_pwd):
            # 原始密码输入正确
            user.set_password(new_pwd)
            user.save()
        else:
            # 原始密码输入不正确  异步方式JsonHttpResponse
            return False
        return '密码修改成功'

    def change_email(self, post, user):
        print('change_email')
        # 获取数据
        new_email = post['new_email']
        password = post['my_pwd']
        # 验证邮箱格式
        if not re.match(r'^[a-z0-9][\w.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$', new_email):
            return 0,'邮箱格式不正确'

        # 校验邮箱是否被绑定
        try:
            user_email_check = User.objects.get(email=new_email)
        except User.DoesNotExist:
            # 邮箱不存在
            user_email_check = None
        if user_email_check:
            # 邮箱已经被绑定
            return 0,'该邮箱已经被绑定'

        if user.check_password(password):
            # 用户原始密码输入正确
            user.email = new_email
            user.save()
        else:
            # 用户密码输入不正确，异步方式JsonHttpResponse
            return 0,'输入的密码不正确'
        return 1, '邮箱修改成功'

class UserGeneView(LoginRequiredMixin, View):
    '''用户中心个人信息页'''
    def get(self, request):
        select = request.GET.get('select')
        user = request.user
        if select == '1':
            genebooks = user.genebook_set.filter(audit_status=1).order_by('-create_time')
        elif select == '2':
            genebooks = user.genebook_set.filter(audit_status=2).order_by('-create_time')
        elif select == '3':
            genebooks = user.genebook_set.filter(audit_status=3).order_by('-create_time')
        elif select == '4':
            genebooks = user.genebook_set.filter(audit_status=4).order_by('-create_time')
        else:
            select = '0'
            genebooks = user.genebook_set.all().order_by('-create_time')

        page = request.GET.get('page')
        pageobj = Page(genebooks, 8, page)
        context = pageobj.paging()
        context['select'] = int(select)

        return render(request, 'user_center_gene.html',context)

class ChangePwdView1(View):
    '''用户中心修改密码'''
    def post(self, request):

        old_pwd = request.POST.get('old_pwd')
        new_pwd = request.POST.get('pwd')
        user = request.user

        if user.check_password(old_pwd):
            # 原始密码输入正确
            user.set_password(new_pwd)
            user.save()
        else:
            # 原始密码输入不正确  异步方式JsonHttpResponse
            return JsonResponse({'res': 1,'errmsg': '原始密码输入不正确'})

        # 跳转到登录界面，让用户重新登录
        return redirect(reverse('user:login'))

class ChangeEmailView(View):
    '''修改绑定的邮箱'''
    def post(self, request):
        '''修改邮箱'''
        # 获取数据
        new_email = request.POST.get('new_email')
        password = request.POST.get('pwd')
        user = request.user

        print(new_email)
        print(password)

        # 验证邮箱格式
        if not re.match(r'^[a-z0-9][\w.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$', new_email):
            return JsonResponse({'res': 1,'errmsg': '邮箱格式不正确'})

        if user.check_password(password):
            # 用户原始密码输入正确
            user.email = new_email
            print(user.email)
            print(user.password)
            # user.save()
        else:
            # 用户密码输入不正确，异步方式JsonHttpResponse
            return JsonResponse({'res': 2,'errmsg': '输入的密码不正确'})
        return JsonResponse({'res': 3,'successmsg': '邮箱修改成功'})