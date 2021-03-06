"""eyagi URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.conf.urls import include, url
from django.contrib import admin
from app import views
from django.contrib.auth import views as auth_views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^login/', auth_views.login, {'template_name':'index.html'},name='login'),
    url(r'^logout/', views.Logouts),
    url(r'^register/$', views.Register, name ='register'),
    url(r'^userinfochange/$', views.User_Change, name = 'userchange'),
    url(r'^passwordchange/$', views.Password_Change, name = 'passwordchange'),
    url(r'^search/', views.Search),
    url(r'^email/', views.Emailsending),
    url(r'^emailaccept/', views.EmailAccept),
    url(r'^(?P<post_id>\d+)/$', views.ViewPost),
    url(r'^tag/(?P<tag>\d+)/$', views.ViewTag),
    url(r'^$', views.Index),
    url(r'^write/$', views.Write, name = 'write'),
    url(r'^comment/$', views.Add_comment, name = 'comment'),
    url(r'^cmt/delete/(?P<post_id>\d+)/(?P<cmt_id>\d+)/$', views.Delete_comment),
] + static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)
