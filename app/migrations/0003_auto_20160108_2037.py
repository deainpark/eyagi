# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-01-08 11:37
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_userinfo'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userinfo',
            name='email',
        ),
        migrations.RemoveField(
            model_name='userinfo',
            name='name',
        ),
        migrations.RemoveField(
            model_name='userinfo',
            name='password',
        ),
    ]
