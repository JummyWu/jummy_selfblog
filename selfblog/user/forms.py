# coding:utf-8

from django.forms import ModelForm

from django.contrib.auth.models import User
from django.contrib.auth.forms import UsernameField


class OauthEditUsernameForm(ModelForm):
    class Meta:
        model = User
        fields = ['username']
        field_classes = {'username': UsernameField}
