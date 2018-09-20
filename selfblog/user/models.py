# coding:utf-8

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Profile(models.Model):
    '''
    用户资料
    '''
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='用户')
    avatar = models.ImageField(upload_to='user/avatar', max_length=200, null=True, blank=True, verbose_name='头像')
    github_id = models.PositiveIntegerField('GitHub id', unique=True, null=True, blank=True)
    new_notice = models.BooleanField('新的通知', default=False)
    read_notice = models.DateTimeField('已读通知', auto_now_add=True)
    blog = models.CharField(max_length=100, null=True, blank=True, verbose_name='用户博客地址')
    bio = models.CharField(max_length=200, null=True, blank=True, verbose_name='用户的简介')
    html = models.CharField(max_length=255, null=True, blank=True, verbose_name='用户github地址')
    location = models.CharField(max_length=255, null=True, blank=True, verbose_name='用户所在地址')
    created_time = models.DateTimeField(auto_now_add=True, null=True, blank=True, verbose_name='创建时间')

    def __str__(self):
        return str(self.pk)

    def get_new_notice(self):
        if not self.new_notice:
            self.new_notice = True
            self.save()

    def have_read_notice(self):
        if self.new_notice:
            self.new_notice = False
            self.read_notice = timezone.now()
            self.save()

    class Meta:
        verbose_name = verbose_name_plural = '用户资料'
