# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from .models import PostComment
from selfblog.custom_site import custom_site
from selfblog.custom_admin import BaseOwnerAdmin


@admin.register(PostComment, site=custom_site)
class PostAdmin(BaseOwnerAdmin):
    list_display =['user', 'content']
