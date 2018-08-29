# coding:utf-8
from __future__ import unicode_literals

from django.contrib import admin

from .models import Comment
from selfblog.custom_site import custom_site
from selfblog.custom_admin import BaseOwnerAdmin


@admin.register(Comment, site=custom_site)
class CommentAdmin(BaseOwnerAdmin):
    list_display = [
        'target', 'nickname', 'content',
        'website', 'created_time'
    ]
