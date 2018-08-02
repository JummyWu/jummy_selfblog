# coding: utf-8
from django.conf.urls import url

from .views import post_list, post_detail


urlpatterns = [
    url(r'^$', post_list, name='index'),
    url(r'^category/(?P<category_id>\d+)/', post_list, name='category'),
    url(r'^tag/(?P<tag_id>\d+)/$', post_list, name='tag'),
    url(r'^post/(?P<pk>\d+).html$', post_detail, name='detail'),
]
