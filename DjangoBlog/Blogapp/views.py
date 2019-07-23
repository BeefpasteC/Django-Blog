import hashlib

from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.core.paginator import Paginator #django开发的分页模块
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response


from Blogapp.models import *
# Create your views here.



# 添加数据
def add_data(request):
    # 添加一百条数据
    for i in range(10):
        data = Blog()
        data.title = "我是 老 %s"%i
        data.content = "I am %s"%i
        data.description = "俺是 老 %s"%i
        data.author = Author.objects.get(id = 1) # id为的作者
        data.save()
        data.type.add(
            Type.objects.get(id = 1)
        ) # id为1的文章类型
        data.save()
    return HttpResponse('save success !')

# 内容列表
# python
def python_list(request,p=1):
    p = int(p)
    # 按照id对数据进行降序
    blogs = Blog.objects.order_by('-id')
    # 将分页的总数据以及每页的条数放入分页模块
    paginator = Paginator(blogs,6)
        # paginator.count #总条数 100
        # paginator.num_pages #总页数
        # paginator.page_range #页码列表
    # 获取具体页的数据
    pagedata = paginator.page(p)
        # page.has_next() 是否由下一页
        # page.has_previous 是否由上一页
        # page.has_other 是否还有数据
    # 获取页码
    start = p-3
    end = p+2
    if start<=0:
        start = 0
    page_range = paginator.page_range[start:end]
    return render_to_response('blogapp/python_list.html',locals())

# mysql
def mysql_list(request,p=1):
    p = int(p)
    # 按照id对数据进行降序
    blogs = Blog.objects.order_by('-id')
    # 将分页的总数据以及每页的条数放入分页模块
    paginator = Paginator(blogs,6)
        # paginator.count #总条数 100
        # paginator.num_pages #总页数
        # paginator.page_range #页码列表
    # 获取具体页的数据
    pagedata = paginator.page(p)
        # page.has_next() 是否由下一页
        # page.has_previous 是否由上一页
        # page.has_other 是否还有数据
    # 获取页码
    start = p-3
    end = p+2
    if start<=0:
        start = 0
    page_range = paginator.page_range[start:end]
    return render_to_response('blogapp/mysql_list.html',locals())

# linux
def linux_list(request,p=1):
    p = int(p)
    # 按照id对数据进行降序
    blogs = Blog.objects.order_by('-id')
    # 将分页的总数据以及每页的条数放入分页模块
    paginator = Paginator(blogs,6)
        # paginator.count #总条数 100
        # paginator.num_pages #总页数
        # paginator.page_range #页码列表
    # 获取具体页的数据
    pagedata = paginator.page(p)
        # page.has_next() 是否由下一页
        # page.has_previous 是否由上一页
        # page.has_other 是否还有数据
    # 获取页码
    start = p-3
    end = p+2
    if start<=0:
        start = 0
    page_range = paginator.page_range[start:end]
    return render_to_response('blogapp/linux_list.html',locals())

# django
def django_list(request,p=1):
    p = int(p)
    # 按照id对数据进行降序
    blogs = Blog.objects.order_by('-id')
    # 将分页的总数据以及每页的条数放入分页模块
    paginator = Paginator(blogs,6)
        # paginator.count #总条数 100
        # paginator.num_pages #总页数
        # paginator.page_range #页码列表
    # 获取具体页的数据
    pagedata = paginator.page(p)
        # page.has_next() 是否由下一页
        # page.has_previous 是否由上一页
        # page.has_other 是否还有数据
    # 获取页码
    start = p-3
    end = p+2
    if start<=0:
        start = 0
    page_range = paginator.page_range[start:end]
    return render_to_response('blogapp/django_list.html',locals())


# 具体内容
def new(request,id):
    id = int(id)
    article = Blog.objects.get(id=id)
    return render_to_response('blogapp/article.html',locals())



# 登录，注册

# 密码加密
def setpassword(password):

    md5 = hashlib.md5()
    md5.update(password.encode())
    return md5.hexdigest()

# cookie和session进行混合校验
def cookie_session(fun):
    '''
    进行登录校验,如果cookie当中的username和session当中的username不一致，
    认为用户不合法。
    '''
    def inner(request,*args,**kwargs):
        cookie_user = request.COOKIES.get('username')
        session_user = request.session.get('username')
        if cookie_user and session_user:
            user = SignData.objects.filter(username=cookie_user).first()
            if user and session_user == cookie_user:
                return fun(request,*args,**kwargs)
        return HttpResponseRedirect('/blog/in')
    return inner

# 首页 cookie校验编写装饰器,校验失败，不能登录。
@cookie_session
def index(request):

    return render(request,'blogapp/python_list.html',locals())



# 登录
def signin(request):
    result = {'content': ''}
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        if not username:
            result["content"] = "用户名不可以为空"
        elif not password:
            result["content"] = "密码不可以为空"
        else:
            user = SignData.objects.filter(username=username).first()
            if user:
                if setpassword(password) == user.password:
                    response = HttpResponseRedirect('/blog/index')
                    response.set_cookie('username', user.username) # 设置cookie值
                    request.session['username'] = user.username # 设置session码
                    return response
                else:
                    result["content"] = "密码错误"
            else:
                result["content"] = "用户名不存在"
    return render(request,'blogapp/signin.html',locals())



# 注册
def signup(request):
    result ={'content':'','status':''}
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        if not username:
            result['content'] = '用户名不可以为空'
        elif not password:
            result['content'] = '密码不可以为空'
        else:
            if not signup_ajax(username):
                user = SignData()
                user.username = username
                user.password = setpassword(password)
                user.save()
                return HttpResponseRedirect('/blog/in')
            else:
                result['content'] = '用户名重复'

    return render(request,'blogapp/signup.html',locals())


# 校验注册用户名重复
def signup_ajax(username):
    user = SignData.objects.filter(username=username).first()
    return user

def signup_ajax_username(request):
    result ={'content':'','status':'error'}
    username = request.POST.get('username')
    if username:
        if username:
            result['content'] = '用户名重复'
        else:
            result["status"] = "success"

    return JsonResponse(result)

# 退出 删除cookie码
def logout(request):
    response = HttpResponseRedirect("/blog/in/")
    response.delete_cookie("username")
    return response




# Create your views here.
