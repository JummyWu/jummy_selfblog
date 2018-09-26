# coding: utf-8
from django import forms
from django.forms import HiddenInput

from .models import PostComment, PostCommentReply


class PostCommentForm(forms.ModelForm):
    class Meta:
        model = PostComment
        fields = ['content', 'article']
        widgets = {
            'article': HiddenInput,
            'content': forms.Textarea(attrs={'placeholder': '请输入评论内容', 'id': 'L_content',
                'lay-verify': 'required', 'class': 'layui-textarea fly-editor',
                'style': 'height: 150px;'})
        }


class PostCommentReplyForm(forms.ModelForm):
    class Meta:
        model = PostCommentReply
        fields = ['content', 'comment', 'reply']
        widgets = {
            'comment': HiddenInput,
            'reply': HiddenInput,
        }
