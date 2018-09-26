# coding: utf-8
from django.conf.urls import url

from .views import CommentView


urlpatterns = [
    url(r'comment/$', CommentView.as_view(), name='comment'),
]
