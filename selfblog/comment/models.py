# coding: utf-8

import markdown
from django.db import models
from django.contrib.auth.models import User
from blog.models import Post


class BaseComment(models.Model):
    '基础评论模型'
    content = models.TextField('评论', max_length=500)
    html = models.TextField(verbose_name='渲染后的数据', default='')
    time = models.DateTimeField('评论时间', auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='评论者')

    def __str__(self):
        return self.content[:10]

    def save(self, *args, **kwargs):
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
        return super(BaseComment, self).save(*args, **kwargs)

    class Meta:
        abstract = True


class PostComment(BaseComment):
    '文章评论'
    article = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments', verbose_name='评论文章')

    class Meta:
        ordering = ['-time']
        verbose_name = '文章评论'
        verbose_name_plural = '文章评论'


class PostCommentReply(BaseComment):
    '文章评论回复(二级评论)'
    comment = models.ForeignKey(PostComment, on_delete=models.CASCADE, related_name='replies', verbose_name='一级评论')
    reply = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, verbose_name='回复对象')

    class Meta:
        ordering = ['time']
        verbose_name = '文章评论回复'
        verbose_name_plural = '文章评论回复'
