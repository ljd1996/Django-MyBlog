# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


class Article(models.Model):
    userId = models.IntegerField(null=False)
    title = models.CharField(max_length=32, null=False)
    content = models.TextField(null=False)
    time = models.DateTimeField(auto_now=True)
