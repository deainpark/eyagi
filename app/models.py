from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.template.defaultfilters import default
# Create your models here.
class UserInfo(models.Model):
    user = models.ForeignKey(User)
    nickname = models.CharField(max_length = 200)
    aftersay=models.TextField(max_length = 500, blank=True)
    emailaccept= models.BooleanField(default=False)
    
    def __unicode__(self):
        return ''+ self.nickname

class Tag(models.Model):
    tags = models.TextField(max_length=100)

    def __unicode__(self):
        return ''+ self.tags

class Category(models.Model):
    category  = models.CharField(max_length=100)
    def __unicode__(self):
        return ''+ self.category

class Post(models.Model):
    user = models.ForeignKey(User)
    title = models.CharField(max_length = 500)
    image = models.ImageField(upload_to = '%y/%m/%d', blank = True)
    posts = models.TextField(max_length = 2000)
    created = models.DateTimeField(auto_now_add=True)
    taged  = models.ManyToManyField(Tag)

    #category = models.ForeignKey(Category)

    def __unicode__(self):
        return ''+ self.title

class Comment(models.Model):
    user = models.ForeignKey(User)
    post = models.ForeignKey(Post)
    comment = models.TextField(max_length= 20)

    def __unicode__(self):
        return ''+ self.comment

