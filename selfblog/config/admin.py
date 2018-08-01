# coding:utf-8
from __future__ import unicode_literals

from django.contrib import admin

from .models import Link, SideBar
from selfblog.custom_site import custom_site
from selfblog.custom_admin import BaseOwnerAdmin


@admin.register(Link, site=custom_site)
class LinkAdmin(BaseOwnerAdmin):
    list_display = [
        'title', 'href',
        'status', 'weight',
        'created_time'
    ]


@admin.register(SideBar, site=custom_site)
class SideBarAdmin(BaseOwnerAdmin):
    list_display = [
        'title', 'display_type',
        'content', 'owner',
        'created_time'
    ]
