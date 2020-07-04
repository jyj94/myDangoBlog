from django.shortcuts import render
from .models import Post, Category
from django.db.models import Q
from django.core.paginator import Paginator
# Create your views here.
def index(request):

    posts = Post.objects.all().order_by('-id')
    paginator = Paginator(posts, 19)
    page_info = request.GET.get('page_info')
    page_info = paginator.get_page(page_info)
    posts = list(page_info)
    post = 0
    if posts :
        post = posts[0]
        posts = posts[1:]
    
    return render(request, 'index.html', {'post':post, 'posts':posts, 'page_info':page_info})

def search(request):
    post_list = Post.objects.all().order_by('-id')
    keyword = request.GET.get('keyword')
    post_result = []
    if keyword:
        #post_result=list(post_list.filter(Q(tag__icontains=keyword)))
        post_result=list(post_list.filter(Q(title__icontains=keyword) | Q(content__icontains=keyword) | Q(tag__icontains=keyword)))
        print(post_result)
    return render(request, 'search.html', {'post_result' : post_result, 'keyword': keyword})

def category(request):
    post_list = Post.objects.all().order_by('-id')
    category = request.GET.get('category')
    category = Category.objects.get(category_name=category)
    post_result=list(post_list.filter(category=category))
    return render(request, 'category.html', {'post_result' : post_result})

def post_view(request):
    post_info = request.GET.get('post_info')
    post = Post.objects.filter(id=post_info)[0]
    print(post)
    print(post_info)
    return render(request, 'post_view.html', {'post':post})

def post_write(request):
    return render(request, 'post_write.html')
