from django.shortcuts import render, redirect
from .models import Post, Category
from django.db.models import Q
from django.core.paginator import Paginator
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.core.files.storage import FileSystemStorage
# Create your views here.
def index(request):
    category_list = Category.objects.all()
    file_system = FileSystemStorage()
    posts = Post.objects.all().order_by('-id')
    paginator = Paginator(posts, 19)
    page_info = request.GET.get('page_info')
    page_info = paginator.get_page(page_info)
    posts = list(page_info)

    for index in range(len(posts)):
        try:
            file_dir = file_system.listdir(posts[index].file_dir)
            for file in file_dir[1:]:
                if "title_image" in file[0]:
                    posts[index].file_dir = posts[index].file_dir + file[0]
        except FileNotFoundError:
            posts[index].file_dir = "1"
        
                

    post = 0
    if posts :
        post = posts[0]
        posts = posts[1:]
    
    
    return render(request, 'index.html', {'post':post, 'posts':posts, 'page_info':page_info, 'category_list' : category_list})

def search(request):
    category_list = Category.objects.all()
    file_system = FileSystemStorage()
    keyword = request.GET.get('keyword')
    if keyword:
        post_list = Post.objects.all().order_by('-id')
        post_list = post_list.filter(Q(title__icontains=keyword) | Q(content__icontains=keyword) | Q(tag__icontains=keyword))

        paginator = Paginator(post_list, 5)
        page_info = request.GET.get('page_info')
        post_list = paginator.get_page(page_info)

        for index in range(len(post_list)):
            try:
                file_dir = file_system.listdir(post_list[index].file_dir)
                for file in file_dir[1:]:
                    if "title_image" in file[0]:
                        post_list[index].file_dir = post_list[index].file_dir + file[0]
            except FileNotFoundError:
                posts[index].file_dir = "1"  

    else:
        post_list = None
    

    return render(request, 'search.html', {'post_list' : post_list, 'keyword': keyword, 'category_list' : category_list})

def category(request):
    category_list = Category.objects.all()
    file_system = FileSystemStorage()
    post_list = Post.objects.all().order_by('-id')
    category = request.GET.get('category')
    category = Category.objects.get(category_name=category)
    post_list = post_list.filter(category=category)

    paginator = Paginator(post_list, 5)
    page_info = request.GET.get('page_info')
    post_list = paginator.get_page(page_info)
    for index in range(len(post_list)):
        try:
        
            file_dir = file_system.listdir(post_list[index].file_dir)
            for file in file_dir[1:]:
                if "title_image" in file[0]:
                    post_list[index].file_dir = post_list[index].file_dir + file[0]
        except FileNotFoundError:
            posts[index].file_dir = "1"           

    return render(request, 'category.html', {'post_list' : post_list, 'category' : category, 'category_list' : category_list})

def post_view(request):
    category_list = Category.objects.all()
    file_system = FileSystemStorage()
    post_info = request.GET.get('post_info')
    post = Post.objects.filter(id=post_info)[0]
    try:
        file_dir = file_system.listdir(post.file_dir)
        for file in file_dir[1:]:
            if "title_image" in file[0]:
                post.file_dir = post.file_dir + file[0]
    except FileNotFoundError:
            posts[index].file_dir = "1"

    return render(request, 'post_view.html', {'post' : post, 'category_list' : category_list})

def post_write(request):
    category_list = Category.objects.all()
    
    if not request.user.is_authenticated: #로그인 여부 검사
        return redirect('index')

    if not request.GET: #새로 작성
        edit_flag = 0
        if not request.POST: #글작성x
            return render(request, 'post_write.html', {'edit_flag':edit_flag, 'category_list' : category_list})
        else: #글 작성 0
            title = request.POST['title']
            content = request.POST['content']
            tag = request.POST['tag']
            category = Category.objects.get(category_name = request.POST['category'])
            author = request.user
            post = Post(title=title, author=author, content=content, category=category, tag=tag, file_dir="1")
            post.save()
            print(post.id)
            post.file_dir = "posts/" + str(post.id) + "/"
            post.save()

            if request.FILES: #post_img가 있을 때
                post_img = request.FILES.get('post_img')
                fs = FileSystemStorage()
                if post_img.content_type == 'image/jpeg':
                    filename = fs.save(post.file_dir+'/'+"title_image.jpg", post_img)
                if post_img.content_type == 'image/png':
                    filename = fs.save(post.file_dir+'/'+"title_image.png", post_img)
                if post_img.content_type == 'image/gif':
                    filename = fs.save(post.file_dir+'/'+"title_image.gif", post_img)

            return redirect('index')
    else: #수정
        edit_flag = 1
        post = Post.objects.get(id = request.GET['post_info'])
        if not request.POST: #글작성x
            return render(request, 'post_write.html', {'edit_flag':edit_flag, 'post':post, 'category_list' : category_list})
        else: #글 작성 0
            post.title = request.POST['title']
            post.content = request.POST['content']
            post.tag = request.POST['tag']
            post.category = Category.objects.get(category_name = request.POST['category'])
            post.save()
            return redirect('index')

def my_login(request):
    alert_flag = False
    category_list = Category.objects.all()
    username = request.POST.get('username')
    password = request.POST.get('password')
    user = authenticate(username = username, password = password)
    if user is not None:
        login(request, user)
        return redirect('index')
    else:
        if username is not None:
            alert_flag = True
        return render(request, 'login.html', {'category_list' : category_list, 'alert_flag' : alert_flag})

def my_logout(request):
    logout(request)
    return redirect('index')

def post_edit(request):
    category_list = Category.objects.all()
    post_id = request.GET.get('post_info')
    post = Post.objects.get(id=post_id)
    
    return render(request, 'post_edit.html', {'category_list' : category_list, 'post' : post})