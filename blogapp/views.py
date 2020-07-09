from django.shortcuts import render, redirect
from .models import Post, Category
from django.db.models import Q
from django.core.paginator import Paginator
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
# Create your views here.
def img_save(request, post_id, post_img, type, body_img_count):
    file_system = FileSystemStorage()
    if type == 1: #타이틀 생성
        if post_img.content_type == 'image/jpeg':
	        file_system.save("posts/" + str(post_id) + "/title_image.jpg", post_img)
        if post_img.content_type == 'image/gif':
            file_system.save("posts/" + str(post_id) + "/title_image.gif", post_img)
        if post_img.content_type == 'image/png':
            file_system.save("posts/" + str(post_id) + "/title_image.png", post_img)
    else: #바디 삽입
        if request.GET:#수정
            if post_img.content_type == 'image/jpeg':
                file_system.save("posts/" + str(post_id) + "/" + str(body_img_count)  + ".jpg", post_img)
            if post_img.content_type == 'image/gif':
                file_system.save("posts/" + str(post_id) + "/" + str(body_img_count)  + ".gif", post_img)
            if post_img.content_type == 'image/png':
                file_system.save("posts/" + str(post_id) + "/" + str(body_img_count)  + ".png", post_img)
        else:  #생성temp
            if post_img.content_type == 'image/jpeg':
                file_system.save("posts/temp/temp" + str(post_id) + "/" + str(body_img_count)  + ".jpg", post_img)
            if post_img.content_type == 'image/gif':
                file_system.save("posts/temp/temp" + str(post_id) + "/" + str(body_img_count)  + ".gif", post_img)
            if post_img.content_type == 'image/png':
                file_system.save("posts/temp/temp" + str(post_id) + "/" + str(body_img_count)  + ".png", post_img)
	



#request function
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
            for file in file_dir[1]:
                if "title_image" in file:
                    posts[index].file_dir = posts[index].file_dir + file
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

        paginator = Paginator(post_list, 19)
        page_info = request.GET.get('page_info')
        post_list = paginator.get_page(page_info)

        for index_number in range(len(post_list)):
            try:
                file_dir = file_system.listdir(post_list[index_number].file_dir)
                for file in file_dir[1]:
                    if "title_image" in file:
                        post_list[index_number].file_dir = post_list[index_number].file_dir + file
            except FileNotFoundError:
                post_list[index_number].file_dir = "1"   
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
    for index_number in range(len(post_list)):
        try:
            file_dir = file_system.listdir(post_list[index_number].file_dir)
            for file in file_dir[1]:
                if "title_image" in file:
                    post_list[index_number].file_dir = post_list[index_number].file_dir + file
        except FileNotFoundError:
            post_list[index_number].file_dir = "1"           

    return render(request, 'category.html', {'post_list' : post_list, 'category' : category, 'category_list' : category_list})

def post_view(request):
    category_list = Category.objects.all()
    file_system = FileSystemStorage()
    post_info = request.GET.get('post_info')
    post = Post.objects.filter(id=post_info)[0]
    try:
        file_dir = file_system.listdir(post.file_dir)
        for file in file_dir[1]:
            if "title_image" in file:
                post.file_dir = post.file_dir + file
    except FileNotFoundError:
            post.file_dir = "1"

    return render(request, 'post_view.html', {'post' : post, 'category_list' : category_list})

def post_write(request):
    category_list = Category.objects.all()
    
    if not request.user.is_authenticated: #로그인 여부 검사
        return redirect('index')

    if request.FILES.get("body_img") and request.POST['delete_flag'] == '0':#바디 삽입
        if request.GET: #수정 모드(디렉토리 있음)
            img_save(request, request.GET['post_info'], request.FILES["body_img"], 0, request.POST['body_img_count'])
        else: #생성 모드(디렉토리 없음) 
            body_img_count = int(request.POST['body_img_count'])
            file_system = FileSystemStorage()
            dir_count = 0
            if body_img_count == 0: #디렉토리 중복 없이 생성
                file_dir = file_system.listdir("posts/temp")
                if file_dir[0] == []:
                    dir_count = 0
                else:
                    for dir in file_dir[0]:
                        if int(dir[4:]) >= dir_count:
                            dir_count = int(dir[4:]) + 1
            else:#가장 높은 dir 찾기
                file_dir = file_system.listdir("posts/temp")
                for dir in file_dir[0]: 
                    if int(dir[4:]) > dir_count:
                        dir_count = int(dir[4:])
            img_save(request, dir_count, request.FILES["body_img"], 0, request.POST['body_img_count'])
        if request.FILES.get("body-img") and request.POST['delete_flag'] == '1':#바디 삭제
            print("추후 생성")
        return HttpResponse("return this string")
        
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
                img_save(request, post.id, post_img, 1, 0)
            return redirect('index')
    else: #수정
        edit_flag = 1
        post = Post.objects.get(id = request.GET['post_info'])
        if not request.POST: #글작성x
            post.content = post.content.replace('\r\n', '\n')
            post.content = post.content.split('\n',)
            return render(request, 'post_write.html', {'edit_flag':edit_flag, 'post':post, 'category_list' : category_list})
        else: #글 작성 0
            post.title = request.POST['title']
            post.content = request.POST['content']
            post.tag = request.POST['tag']
            post.category = Category.objects.get(category_name = request.POST['category'])
            post.save()
            if request.FILES.get('post_img'):
                post_img = request.FILES.get('post_img')
                file_system = FileSystemStorage()
                post_dir_not_found = True
                for post_id in file_system.listdir("posts"):
                    for post_id_id in post_id:
                        if str(post.id) == post_id_id:
                            post_dir_not_found = False
                if post_dir_not_found == False:
                    file_dir = file_system.listdir(post.file_dir)
                    if file_dir[1] != []:
                        for file in file_dir[1:]:
                            if "title_image" in file[0]:
                                file_system.delete(post.file_dir + str(file[0]))
                img_save(request, post.id, post_img, 1, 0)
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

