from django.db import models

# Create your models here.

class Post(models.Model):
    title = models.CharField(max_length=100, null=False)
    author = models.CharField(max_length=10, null=False)
    pub_date = models.DateTimeField(auto_now_add=True)
    file_dir = models.CharField(max_length=100, null=False)
    content = models.TextField()
