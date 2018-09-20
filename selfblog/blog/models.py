# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import markdown

from django.db.models import F
from django.contrib.auth.models import User
from django.db import models

# Create your models here.
STATUS_ITEMS = (
    (1, '正常'),
    (2, '删除'),
)


class Post(models.Model):
    title = models.CharField(max_length=50, verbose_name='标题')
    desc = models.CharField(max_length=255, blank=True, verbose_name="摘要")
    category = models.ForeignKey('Category', verbose_name="分类", on_delete=models.DO_NOTHING)
    tags = models.ManyToManyField('Tag', related_name='posts', verbose_name="标签")

    content = models.TextField(verbose_name="内容", help_text="注：目前仅支持Markdown格式数据")
    html = models.TextField(verbose_name='渲染后的数据', default='', help_text="目前支持markdown")
    is_markdown = models.BooleanField(verbose_name='是否使用markdown', default=True)
    status = models.IntegerField(default=1, choices=STATUS_ITEMS, verbose_name="状态")
    owner = models.ForeignKey(User, verbose_name="作者", on_delete=models.DO_NOTHING)
    pv = models.PositiveIntegerField(default=0, verbose_name='pv')
    uv = models.PositiveIntegerField(default=0, verbose_name='uv')
    created_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")

    def status_show(self):
        return '当前状态:{}'.format(self.status)
    status_show.short_description = '展示状态'

    def __str__(self):
        return self.title

    def increse_pv(self):
        return type(self).objects.filter(id=self.id).update(pv=F('pv') + 1)

    def increse_uv(self):
        return type(self).objects.filter(id=self.id).update(pv=F('uv') + 1)

    def save(self, *args, **kwargs):
        if self.is_markdown:
            config = {
                'codehilite': {
                    'use_pygments': False,
                    'css_class': 'prettyprint linenums code-padding',
                }
            }
            self.html = markdown.markdown(
                self.content,
                extensions=["codehilite", "fenced_code", "nl2br"],
                extension_configs=config
            )
        else:
            self.html = self.content
        return super(Post, self).save(*args, **kwargs)

    class Meta:
        verbose_name = verbose_name_plural = "文章"
        ordering = ['-id']


class Category(models.Model):
    name = models.CharField(max_length=50, verbose_name="名称")
    status = models.PositiveIntegerField(default=1, choices=STATUS_ITEMS, verbose_name="状态")
    is_nav = models.BooleanField(default=False, verbose_name="是否为导航")

    owner = models.ForeignKey(User, verbose_name="作者", on_delete=models.DO_NOTHING)
    created_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = verbose_name_plural = '分类'


class Tag(models.Model):
    name = models.CharField(max_length=10, verbose_name="名称")
    status = models.PositiveIntegerField(default=1, choices=STATUS_ITEMS, verbose_name="状态")

    owner = models.ForeignKey(User, verbose_name="作者", on_delete=models.DO_NOTHING)
    created_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = verbose_name_plural = '标签'
