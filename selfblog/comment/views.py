# coding:utf-8
from __future__ import unicode_literals

from django.views.generic import TemplateView
from django.shortcuts import redirect

from .models import PostComment
from .forms import PostCommentForm


class CommentShowMixin(object):
    def get_comments(self):
        article = self.kwargs['pk']
        comments = PostComment.objects.filter(article=article)
        return comments

    def get_context_data(self, **kwargs):
        kwargs.update({
            'comment_form': PostCommentForm(initial={'article': self.kwargs['pk']}),
            'comment_list': self.get_comments(),
        })
        return super(CommentShowMixin, self).get_context_data(**kwargs)


class CommentView(TemplateView):
    http_method_names = ['post']
    template_name = 'comment/post_comment.html'

    def post(self, request, *args, **kwargs):
        comment_form = PostCommentForm(request.POST)
        article = request.POST.get('article')
        post = request.POST.get('post')

        if comment_form.is_valid():
            instance=comment_form.save(commit=False)
            instance.article.pk = article
            instance.user_id = request.user.id
            instance.save()
            succeed = True
            print(type(post))
            return redirect(post)
        else:
            succeed = False
        context = {
            'succeed': succeed,
            'form': comment_form,
            'article': article,
        }
        return self.render_to_response(context)
