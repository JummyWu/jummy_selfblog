# coding: utf-8
from django.conf.urls import url, include
from django.views.decorators.cache import cache_page

from .views import IndexView, CategoryView, TagView, PostView


urlpatterns = [
    url(r'^$', IndexView.as_view(), name='index'),
    url(r'^category/(?P<category_id>\d+)/', cache_page(60 * 10)(CategoryView.as_view()), name='category'),
    url(r'^tag/(?P<tag_id>\d+)/$', TagView.as_view(), name='tag'),
    url(r'^post/(?P<pk>\d+)/$', PostView.as_view(), name='detail'),
    url(r'^search/', include('haystack.urls'))
]
