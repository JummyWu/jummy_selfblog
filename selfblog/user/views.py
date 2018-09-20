# conding:utf-8

import requests

from django.http import HttpResponseRedirect
from django.contrib.auth import logout
from django.shortcuts import redirect, reverse
from django.core.exceptions import PermissionDenied
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LogoutView
from django.views.generic import View, TemplateView, FormView
from django.views.decorators.csrf import ensure_csrf_cookie
from django.utils.decorators import method_decorator

from django.conf import settings
from .forms import OauthEditUsernameForm
from .models import Profile


class HomeView(LoginRequiredMixin, TemplateView):
    template_name = 'user/home.html'


class LogoutView(LogoutView):

    def dispatch(self, request, *args, **kwargs):
        logout(request)
        next = request.GET.get('next')
        if next == '/user/home/':
            next_page = settings.LOGOUT_REDIRECT_URL
            if next_page:
                return HttpResponseRedirect(next_page)
        else:
            next_page = self.get_next_page()
            if next_page:
                return HttpResponseRedirect(next_page)
        return super().dispatch(request, *args, **kwargs)


@method_decorator(ensure_csrf_cookie, name='dispatch')
class OAuthLoginView(TemplateView):
    '第三方登陆视图'
    template_name = 'user/login.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if 'next' in self.request.GET:
            self.request.session['next'] = self.request.GET['next']
            context['github_oauth_url'] = 'https://github.com/login/oauth/authorize?client_id={}&state={}' \
.format(settings.GITHUB_CLIENT_ID, self.request.META['CSRF_COOKIE'])
        return context


class OathView(View):
    access_token_url = None
    user_api = None
    client_id = None
    client_secret = None

    def get(self, request, *args, **kwargs):
        access_token = self.get_access_token(request)
        user_info = self.get_user_info(access_token)
        return self.authenticate(user_info)

    def get_access_token(self, request):
        '获取access token'
        url = self.access_token_url
        headers = {'Accept': 'application/json'}
        data = {
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'code': request.GET['code']
        }
        r = requests.post(url, data, headers=headers, timeout=1)
        result = r.json()
        if 'access_token' in result:
            return result['access_token']
        else:
            raise PermissionDenied

    def get_user_info(self, access_token):
        '获取用户信息'
        url = self.user_api + access_token
        r = requests.get(url, timeout=1)
        user_info = r.json()
        return user_info

    def get_success_url(self):
        '获取登录成功后返回的网页'
        if 'next' in self.request.session:
            return self.request.session.pop('next')
        else:
            # 没有next就只能返回主页
            return '/'


class GitHubOAuthView(OathView):
    access_token_url = settings.GITHUB_ACCESS_TOKEN_URL
    user_api = settings.GITHUB_USER_API
    client_id = settings.GITHUB_CLIENT_ID
    client_secret = settings.GITHUB_CLIENT_SECRET

    def authenticate(self, user_info):
        user = User.objects.filter(profile__github_id=user_info['id'])
        if not user:
            if User.objects.filter(username=user_info['login']).exists():
                self.request.session['github_oauth'] = user_info
                return redirect(reverse('user:edit_name'))
            user = User.objects.create_user(user_info['login'], user_info['email'])
            profile = Profile(user=user, github_id=user_info['id'], avatar=user_info['avatar_url'],
                    blog=user_info['blog'], bio=user_info['bio'], html=user_info['html_url'], location=user_info['location'])
            profile.save()
        else:
            user = user[0]
        login(self.request, user)
        return redirect(self.get_success_url())


class OAuthEditUsername(FormView):
    '通过第三方账户注册时，用户名若重复，则通过该视图修改合适的用户名'
    template_name = 'user/edit_name.html'
    form_class = OauthEditUsernameForm

    def dispatch(self, request, *args, **kwargs):
        if 'github_oauth' not in request.session:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['username'] = self.request.session['github_oauth']['login']
        return context

    def form_valid(self, form):
        """If the form is valid, save the associated model."""
        if 'github_oauth' in self.request.session:
            user_info = self.request.session.pop('github_oauth')
            user = form.save()
            profile = Profile(user=user, github_id=user_info['id'], avatar=user_info['avatar_url'])
            profile.save()
            login(self.request, user)
        return super().form_valid(form)

    def get_success_url(self):
        if 'next' in self.request.session:
            return self.request.session.pop('next')
        else:
            return '/'
