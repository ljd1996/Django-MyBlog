# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import models
from django.contrib import admin


class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'content', 'time')
    list_filter = ('time', )


admin.site.register(models.Article, ArticleAdmin)
