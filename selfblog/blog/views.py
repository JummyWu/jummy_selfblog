# coding:utf-8
from __future__ import unicode_literals

from django.views.generic import ListView, DetailView

from .models import Post, Category, Tag
from config.models import SideBar
from comment.models import Comment
from comment.forms import CommentForm


class CommonMixin(object):
    def get_category_context(self):
        categories = Category.objects.filter(status=1)
        nav_cates = []
        cates = []
        for cate in categories:
            if cate.is_nav:
                nav_cates.append(cate)
            else:
                cates.append(cate)
        return {
            'nav_cates': nav_cates,
            'cates': cates,
        }

    def get_context_data(self, **kwargs):
        side_bars = SideBar.objects.filter(status=1)
        recently_posts = Post.objects.filter(status=1)[:10]
        # hot_posts = Post.objects.filter(status=1).order_by('views'){[:10]
        recently_comments = Comment.objects.filter(status=1)[:10]

        kwargs.update({
            'side_bars': side_bars,
            'recently_posts': recently_posts,
            'recently_comments': recently_comments,
        })
        kwargs.update(self.get_category_context())
        return super(CommonMixin, self).get_context_data(**kwargs)


class BaseDateView(CommonMixin, ListView):
    model = Post
    template_name = 'blog/list.html'
    context_object_name = 'posts'
    paginate_by = 3


class IndexView(BaseDateView):
    pass


class CategoryView(BaseDateView):
    def get_queryser(self):
        qs = super(CategoryView, self).get_queryset()
        cate_id = self.kwargs.get('category_id')
        qs = qs.filter(Category_id=cate_id)
        return qs


class TagView(BaseDateView):
    def get_queryser(self):
        tag_id = self.kwargs('tag_id')
        try:
            tag=Tag.objects.get(id=tag_id)
        except Tag.DoesNotExist:
            return []
        posts = tag.posts.all()
        return posts


class AuthorView(BaseDateView):
    def get_queryser(self):
        qs = super(AuthorView, self).get_queryset()
        author_id = self.request.GET.get('author_id')
        if author_id:
            qs = qs.filter(owner_id=author_id)
        return qs


class PostView(DetailView):
    model = Post
    template_name = 'blog/detail.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        kwargs.update({
            'comment_form': CommentForm()
        })
        return super(PostView, self).get_context_data(**kwargs)
