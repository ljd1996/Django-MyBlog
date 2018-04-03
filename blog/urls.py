from django.conf.urls import url
from . import views
from django.contrib.auth.views import login, logout


urlpatterns = [
    url(r'^index/(?P<page>[0-9]+)$', views.index, name='index'),
    url(r'^article/(?P<article_id>[0-9]+)$', views.article_page, name='article_page'),
    url(r'^edit/(?P<article_id>[0-9]+)$', views.edit_page, name='edit_page'),
    url(r'^edit/action/$', views.edit_action, name='edit_action'),
    # url(r'^login/$', views.login),
    url(r'^logout/$', logout),
    url(r'^login/$', views.login, name='login'),
    url(r'^author/$', views.author, name='author'),
    url(r'^delete/$', views.delete, name='delete'),
]