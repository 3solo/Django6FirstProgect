from django.db import models
from django.conf import settings


class UploadFiles(models.Model):
    file = models.FileField(upload_to='uploads_model')


class FloodMessages(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, )
    message = models.CharField(max_length=99)
    time_drop = models.DateTimeField(auto_now_add = True)


class News(models.Model):
    title = models.CharField(max_length=40)
    content = models.CharField(max_length=150)
    time_drop = models.DateTimeField(auto_now_add=True)
    photo = models.ImageField(upload_to='news',  blank=True, null=True)


class Category(models.Model):
    name = models.CharField(max_length=40)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)


class Topic(models.Model):
    title = models.CharField(max_length=40)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_time = models.DateTimeField(auto_now_add=True)


class TopicMessages(models.Model):
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    created_time = models.DateTimeField(auto_now_add=True)






