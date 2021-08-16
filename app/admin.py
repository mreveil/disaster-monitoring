# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.contrib import admin
from app.models import Author, Report, KeyValuePair

# Register your models here.
admin.site.register(Author)
admin.site.register(Report)
admin.site.register(KeyValuePair)
