# coding:utf-8
from __future__ import unicode_literals

from django.core.cache import cache
from django.views.generic import ListView, DetailView

from .models import Post, Category, Tag
from config.models import SideBar
from comment.models import Comment


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
        hot_posts = Post.objects.filter(status=1).order_by('-pv')[:10]
        recently_comments = Comment.objects.filter(status=1)[:10]

        kwargs.update({
            'side_bars': side_bars,
            'recently_posts': recently_posts,
            'recently_comments': recently_comments,
            'hot_posts': hot_posts,
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

    def get(self, request, *args, **kwargs):
        response = super(PostView, self).get(request, *args, **kwargs)
        self.pv_uv()
        return response

    def pv_uv(self):
        sessionid = self.request.COOKIES.get('sessionid')
        path = self.request.path

        if not sessionid:
            return

        pv_key = 'pv:{}:{}'.format(sessionid, path)
        if not cache.get(pv_key):
            self.object.increse_pv()
            cache.set(pv_key, 1, 60)

        uv_key = 'uv:{}:{}'.format(sessionid, path)
        if not cache.get(uv_key):
            self.object.increse_uv()
            cache.set(uv_key, 1, 60)
