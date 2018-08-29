# coding:utf-8
from __future__ import unicode_literals

from django.views.generic import ListView

from .models import Link
from blog.views import CommonMixin


class LinkView(CommonMixin, ListView):
    queryset = Link.objects.filter(status=1)
    template_name = 'config/links.html'
    context_object_name='links'
