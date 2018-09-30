# coding: utf-8
from django.conf.urls import url

from .views import LinkView


urlpatterns = [
    url(r'links/$', LinkView.as_view(), name='link'),
]
