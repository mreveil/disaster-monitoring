# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.contrib import admin
from app.models import Author, Report, KeyValuePair, Location, MediaCoverage, KeyEvent

# Register your models here.
admin.site.register(Author)
admin.site.register(Report)
admin.site.register(KeyValuePair)
admin.site.register(Location)
admin.site.register(MediaCoverage)
admin.site.register(KeyEvent)
