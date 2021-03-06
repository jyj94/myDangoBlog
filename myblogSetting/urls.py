"""myblogSetting URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
import blogapp.views 

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', blogapp.views.index, name='index'),
    path('search/', blogapp.views.search, name='search'),
    path('category/', blogapp.views.category, name='category'),
    path('post_view/', blogapp.views.post_view, name='post_view'),
    path('post_write/', blogapp.views.post_write, name='post_write'),
    path('login/', blogapp.views.my_login, name='login'),
    path('logout/', blogapp.views.my_logout, name='logout'),
    path('post_edit/', blogapp.views.post_edit, name='post_edit'),
]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

