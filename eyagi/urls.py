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

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^index/login/', auth_views.login, {'template_name':'login.html'},name='login'),
    url(r'^index/logout/', views.logouts),
    url(r'^index/register/', views.register),
    url(r'^index/search/', views.Search),
    url(r'^index/email/', views.Emailsending),
    url(r'^index/emailaccept/', views.EmailAccept),
    url(r'^index/(?P<post_id>\d+)/$', views.ViewPost),
    url(r'^index/tag/(?P<tag>\w+)/$', views.ViewTag),
    url(r'^index/$', views.index),
    url(r'^index/write/$', views.write, name = 'write'),
    url(r'^index/comment/$', views.add_comment, name = 'comment'),
    url(r'^index/cmt/delete/(?P<post_id>\d+)/(?P<cmt_id>\d+)/$', views.delete_comment),
]
