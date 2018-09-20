# coding:utf-8

from django.conf.urls import url

from .views import LogoutView, HomeView, OAuthLoginView, GitHubOAuthView, OAuthEditUsername


app_name='user'
urlpatterns = [
    url(r'^home/$', HomeView.as_view(), name='home'),
    url(r'^logout/$', LogoutView.as_view(), name='logout'),
    url(r'^login/$', OAuthLoginView.as_view(), name='login'),
    url(r'^oauth/github/$', GitHubOAuthView.as_view(), name='github_oauth'),
    url(r'^oauth/edit_name/$', OAuthEditUsername.as_view(), name='edit_name'),
]
