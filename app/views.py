# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.shortcuts import render, get_object_or_404, redirect,\
    render_to_response
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from app.models import *
from app.forms import *
from django.http.response import HttpResponseRedirect, HttpResponse
from django.db.transaction import commit
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib.auth import authenticate, login, logout
from django.core.urlresolvers import reverse  
from django.core.mail import send_mail  

def logouts(request):
    logout(request)
    
    return render(request, "login.html")

def register(request):
    
    if request.method == 'POST':
        forms = CreateUser(request.POST)
        if forms.is_valid():
            newuser = forms.save()
            newuser.save()
            return HttpResponseRedirect("/index/")
    else:
        forms = CreateUser()
        
    return render(request, "register.html",{'form': forms})

@login_required(login_url='/index/login/')
def User_Info(request):
    user = UserInfo.objects.all().filter(user=request.user)
    postcount = Post.objects.all().filter(user=request.user)
    count = len(postcount)
    
    return render_to_response("userinfo.html",{
                                       'count':count,
                                       'user':user,
                                       } )


def index(request):
    posts = Post.objects.all().order_by('-created')
    pagintor = Paginator(posts, 10)
    
    page = request.GET.get('page')
    
    try:
        ps = pagintor.page(page)
    except PageNotAnInteger:
        ps = pagintor.page(1)
    except EmptyPage:
        ps = pagintor.page(pagintor.num_pages)
    
    return render_to_response("index.html",{
                                       'posts':ps,
                                       } )

@login_required(login_url='/index/login/')
def write(request):
    if request.method == 'POST':
        
        form = Postwrite(request.POST, request.FILES)
        
        if form.is_valid():
            wpost = form.save(commit = False)
            wpost.user = request.user

            wpost.save()
            
            
            return HttpResponseRedirect("/index/")
    else:
        form = Postwrite()
        
    return render(
                  request,
                  'write.html',
                  {
                    'form':form,
                   }
                  )
@login_required(login_url='/index/login/')
def add_comment(request):
    if request.method == "POST":
        if request.POST.has_key('comment'):
            cmt = request.POST['comment']
        if request.POST.has_key('post_id'):
            id = Post.objects.get(pk=int(request.POST['post_id']))
            pid = request.POST['post_id']
        newcmt = Comment(post = id, comment=cmt)
        newcmt.user = request.user
        newcmt.save()
        
        re = "/index/%s/" %pid
        
        return HttpResponseRedirect(re)   
    
@login_required(login_url='/index/login/')
def delete_comment(request,post_id, cmt_id):
    cmt = Comment.objects.get(pk=cmt_id)
    if cmt.user == request.user:
        cmt.delete()
    
    re= "/index/%s/" %post_id
    return HttpResponseRedirect(re) 
    
def ViewPost(request, post_id):
    post = get_object_or_404(Post, pk = post_id)
    cmt = Comment.objects.all().filter(post=post_id)
    
    return render(request,
                    'posts.html', 
                    {
                     'post':post,
                     'cmt':cmt,
                    }
                  )
    
def ViewTag(request, tag):
    tg = Post.objects.all().filter(tags=tag)
    
    
    return render(request, 
                  'tag.html',
                  {
                   'tag':tg
                   }
                  )
    
def Search(request):
    qs= request.GET.get('search')
    query = Post.objects.filter(Q(title__icontains=qs))
        
    return render(request,
                  'search.html',
                  {'query':query}
                  )

def Emailsending(request):
    user = UserInfo.objects.filter(user=request.user)
    sub = 'requirement accept email'
    frommail = 'admin@eyagi.com'
    if request.method == "POST":
        if request.POST.has_key('email'):
            email = request.POST['email']
        if request.POST.has_key('message'):
            message = request.POST['message']
        send_mail(sub, message, frommail, [email])
        return HttpResponse("sending")
    
    return render(request,'userinfo.html',
                  {
                   'user':user
                   })

@login_required(login_url='/index/login/')
def EmailAccept(request):
    userinfo = UserInfo(user = request.user,emailaccept = True )

    userinfo.save()
        
    return HttpResponseRedirect("/index/")