# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.shortcuts import render, get_object_or_404, redirect,\
    render_to_response
from django.contrib.auth.models import User
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

def Logouts(request):
    logout(request)
    
    return HttpResponseRedirect("/login/")

def Register(request):
    warm=""
    if request.method == 'POST':
        if request.POST.has_key('username'):
            name = request.POST['username']
        if request.POST.has_key('email'):
            email = request.POST['email']
        if request.POST.has_key('password1'):
            password1 = request.POST['password1']
        if request.POST.has_key('password2'):
            password2 = request.POST['password2']
            
        if password1 == password2:
            if User.objects.filter(username=name).exists() or User.objects.filter(email=email).exists():
                warm="이미 존재하는 회원입니다."
            else:
                user = User.objects.create_user(name, email, password1)
                user.save()          
                return HttpResponseRedirect("/login/")
        else:
            warm="비밀번호가 일치하지 않습니다."
    return render(request,'register.html', {'warm':warm,})

def Password(request, ps):
    if len(ps) < 8:
        return False
    else:
        return True
'''
def RegisterForm(request):
    if request.method == 'POST':
        forms = CreateUser(request.POST)
        if forms.is_valid():
            newuser = forms.save()
            newuser.save()
            return HttpResponseRedirect("/login/")
    else:
        forms = CreateUser()
    return render(request, "register.html",{'form': forms,})
'''
#사용자
@login_required(login_url='/login/')
def User_Info(request):
    user = UserInfo.objects.filter(user=request.user)
    postcount = Post.objects.all().filter(user=request.user)
    count = len(postcount)
    
    return render_to_response("userinfo.html",{
                                       'count':count,
                                       'user':user,
                                       } )
    
@login_required(login_url='/login/')
def User_Change(request):
	if request.method == 'POST':
		if request.POST.has_key('nickname'):
			nickname = request.POST['nickname']
		if request.POST.has_key('aftersay'):
			aftersay = request.POST['aftersay']

		user = UserInfo(nickname = nickname, aftersay = aftersay)
		user.user = request.user
		user.save()
		return HttpResponse('changed')

@login_required(login_url='/login/')
def Password_Change(request):
	user = User.objects.get(username=request.username)
	if request.method == 'POST': 
		if request.POST.has_key('password'):
			password = request.POST['password']
			user.set_password(password)
			user.save()
			return HttpResponse('changed')

#인덱스
@login_required(login_url='/login/')
def Index(request):
    posts = Post.objects.all().order_by('-created')
    tag = Tag.objects.all()
    pagintor = Paginator(posts, 10)
    page = request.GET.get('page')
    try:
        ps = pagintor.page(page)
    except PageNotAnInteger:
        ps = pagintor.page(1)
    except EmptyPage:
        ps = pagintor.page(pagintor.num_pages)
    logincheck = LoginCheck(request)

    return render_to_response("index.html",{'posts':ps,'tag':tag,'check':logincheck,} )

def LoginCheck(request):
    if request.user.is_authenticated():
        return True
    else:
        return False

#포스트 작성
@login_required(login_url='/login/')
def Write(request):
    if request.method == 'POST':
        form = Postwrite(request.POST, request.FILES)
        if request.POST.has_key('tag'):
            tg = request.POST['tag']
            if tg is "":
                tg = "태그없음"
            
        if form.is_valid():
            wpost = form.save(commit = False)
            wpost.user = request.user
            wpost.save()
            
            if not Tag.objects.filter(tags=tg).exists():
                wtag = Tag(tags=tg)
                wtag.save()
                wtag.posts.add(wpost)
            else:
                wtag_id = Tag.objects.filter(tags=tg)
                wtag = Tag.objects.get(pk=wtag_id)
                wtag.save()
                wtag.posts.add(wpost)
                
            return HttpResponseRedirect("/")

    else:
        form = Postwrite()

    return render(
                  request,
                  'write.html',
                  {
                    'form':form,
                   }
                  )
#코멘트 작성
@login_required(login_url='/login/')
def Add_comment(request):
    if request.method == "POST":
        if request.POST.has_key('comment'):
            cmt = request.POST['comment']
        if request.POST.has_key('post_id'):
            id = Post.objects.get(pk=int(request.POST['post_id']))
            pid = request.POST['post_id']
        newcmt = Comment(post = id, comment=cmt)
        newcmt.user = request.user
        newcmt.save()
        
        re = "/%s/" %pid
        
        return HttpResponseRedirect(re)   

#코멘트 삭제    
@login_required(login_url='/login/')
def Delete_comment(request,post_id, cmt_id):
    cmt = Comment.objects.get(pk=cmt_id)
    if cmt.user == request.user:
        cmt.delete()
    
    re= "/index/%s/" %post_id
    return HttpResponseRedirect(re)
 
#포스트 보기   
def ViewPost(request, post_id):
    post = get_object_or_404(Post, pk = post_id)
    cmt = Comment.objects.all().filter(post=post_id)
    tg  = Tag.objects.filter(post__id=post_id)
    return render(request,
                    'posts.html', 
                    {
                     'post':post,
                     'cmt':cmt,
                    'tag':tg,
                    }
                  )

def ViewTag(request, tag):
    ct = Tag.objects.get(pk=tag)
    ctlist = ct.post.all()
    return render(request, 
                  'tags.html',
                  {
                   'tags':ctlist,
                   }
                  )
#검색    
def Search(request):
    qs= request.GET.get('search')
    query = Post.objects.filter(Q(title__icontains=qs))
        
    return render(request,
                  'search.html',
                  {'query':query}
                  )

#메일 전송
@login_required(login_url='/login/')
def Emailsending(request):
    user = User.objects.get(username=request.username)
    sub = 'requirement accept email'
    if request.method == "POST":
        if request.POST.has_key('message'):
            message = request.POST['message']
        user.email_user(sub, message)
        return HttpResponse("sending")
    
    return render(request,'userinfo.html',
                  {
                   'user':user
                   })

#메일 인증
@login_required(login_url='/login/')
def EmailAccept(request):
    userinfo = UserInfo(user = request.user,emailaccept = True )
    userinfo.save()

    return HttpResponseRedirect("/")