from django.shortcuts import render
from .models import Post
from django.core.paginator import Paginator
# Create your views here.
def index(request):

    posts = Post.objects.all().order_by('-id')
    paginator = Paginator(posts, 19)
    page_info = request.GET.get('page_info')
    page_info = paginator.get_page(page_info)
    posts = list(page_info)
    post = posts[0]
    posts = posts[1:]
    
    return render(request, 'index.html', {'post':post, 'posts':posts, 'page_info':page_info})

def search(request):
    return render(request, 'search.html')

def category(request):
    return render(request, 'category.html')

def post_view(request):
    return render(request, 'post_view.html')

def post_write(request):
    return render(request, 'post_write.html')
