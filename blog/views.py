# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, render_to_response
import models
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.views.decorators.cache import cache_page
from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, permission_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


# @cache_page(60 * 15)
def index(request, page):
    articles_all = models.Article.objects.all()
    paginator = Paginator(articles_all, 3)
    pages = range(1, paginator.num_pages+1)
    try:
        articles = paginator.page(page)
    except PageNotAnInteger:
        articles = paginator.page(1)
    except EmptyPage:
        articles = paginator.page(1)
    return render(request, 'blog/index.html',
                  {'articles': articles, 'pages': pages, 'recordNum': paginator.count})


def login(request):
    if request.method == 'GET':
        return render(request, 'blog/login.html', {'next': request.GET.get('next')})
    else:
        username = request.POST.get('username')
        password = request.POST.get('password')
        loginkeeping = request.POST.get('loginkeeping')
        if loginkeeping:
            request.session.set_expiry(30)
        else:
            request.session.set_expiry(0)
        # user = User.objects.create_user('hearing', '2441692559@qq.com', 'admin123456')
        user = auth.authenticate(username=username, password=password)
        # print(request.session['next'])
        if user is not None and user.is_active:
            auth.login(request, user)
            # user.user_permissions.add(19)
            # user.save()
            url = request.POST.get('next')
            if url == 'None':
                url = '/blog/index/'
            return HttpResponseRedirect(url)
        return render(request, 'blog/login.html',
                      {'error': '用户名或密码错误！', 'next': request.POST.get('next')})


def article_page(request, article_id):
    article = models.Article.objects.get(pk=article_id)
    return render(request, 'blog/article_page.html', {'article': article, 'author': User.objects.get(id=article.userId).username})


# @permission_required('blog.add_article')
@login_required(login_url='/blog/login')
def edit_page(request, article_id):
    if str(article_id) == '0':
        return render(request, 'blog/edit_page.html')
    article = models.Article.objects.get(pk=article_id)
    return render(request, 'blog/edit_page.html', {'article': article})


def edit_action(request):
    title = request.POST.get('title', 'TITLE')
    content = request.POST.get('content', 'CONTENT')

    article_id = request.POST.get('article_id', '0')
    if article_id == '0':
        models.Article.objects.create(userId=request.user.id, title=title, content=content)
        return HttpResponseRedirect('/blog/index/1')
    article = models.Article.objects.get(pk=article_id)
    article.title = title
    article.content = content
    article.save()
    return HttpResponseRedirect('/blog/article/' + article_id)


@login_required(login_url='/blog/login')
def author(request):
    return render(request, 'blog/author.html')


# @login_required(login_url='/blog/login')
def delete(request):
    models.Article.objects.get(pk=request.GET.get('id')).delete()
    # return HttpResponse(json.dump({'result': '删除成功'}), content_type='application/json')
    return JsonResponse({'result': '删除成功'})
