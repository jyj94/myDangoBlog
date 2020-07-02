from django.shortcuts import render
from .models import Post
from django.core.paginator import Paginator
# Create your views here.
def index(request):
    
    posts = Post.objects.all().order_by('-id')
    posts = list(posts)[1:]
    post = Post.objects.last()
    return render(request, 'index.html', {'post':post, 'posts':posts})

def search(request):
    return render(request, 'search.html')

def catagory(request):
    return render(request, 'catagory.html')

def post_view(request):
    return render(request, 'post_view.html')

def post_write(request):
    return render(request, 'post_write.html')
