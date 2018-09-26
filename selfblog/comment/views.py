# coding:utf-8
from __future__ import unicode_literals

from django.views.generic import TemplateView
from django.urls import reverse, NoReverseMatch
from django.core.exceptions import ImproperlyConfigured

from .models import PostComment
from .forms import PostCommentForm


class CommentShowMixin(object):
    def get_comments(self):
        article = self.kwargs['pk']
        comments = PostComment.objects.filter(article=article)
        return comments

    def get_context_data(self, **kwargs):
        content = PostCommentForm()
        content.fields['article'].widget.attrs['value']=self.kwargs['pk']
        kwargs.update({
            'comment_form': content,
            'comment_list': self.get_comments(),
        })
        return super(CommentShowMixin, self).get_context_data(**kwargs)


class CommentView(TemplateView):
    http_method_names = ['post']
    template_name = 'comment/post_comment.html'
