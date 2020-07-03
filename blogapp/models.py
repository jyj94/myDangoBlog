from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Post(models.Model):
    title = models.CharField(max_length=100, null=False)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, default=1)
    pub_date = models.DateTimeField(auto_now_add=True)
    file_dir = models.CharField(max_length=100, null=False)
    content = models.TextField()
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    tag = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.title
    
class Category(models.Model):
    category_name = models.CharField(max_length=100, null=False)

    def __str__(self):
        return self.category_name
    