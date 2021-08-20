# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.db import models
from django.contrib.auth.models import User
from datetime import datetime


class Author(models.Model):
    name = models.CharField(max_length=50)
    affiliation = models.CharField(max_length=50, blank=True, null=True)
    profile_link = models.CharField(max_length=250)
    affiliation_link = models.CharField(max_length=250, blank=True, null=True)

    def __str__(self):
        return "%s" % (self.name)

    class Meta:
        unique_together = ["profile_link"]


class MediaCoverage(models.Model):
    media_name = models.CharField(max_length=50)
    pub_link = models.CharField(max_length=250)
    pub_time = models.DateTimeField()
    authors = models.CharField(max_length=250)
    title = models.CharField(max_length=100, default="")
    description = models.CharField(max_length=500, default="")
    image = models.ImageField(default=None, null=True, blank=True)


class KeyEvent(models.Model):
    author = models.ForeignKey(Author, on_delete=models.SET_NULL, null=True)
    pub_time = models.DateTimeField()
    pub_link = models.CharField(max_length=250)
    title = models.CharField(max_length=100, null=True)
    embed_code = models.CharField(max_length=1000)
    description = models.CharField(max_length=250, null=True, blank=True)


class KeyValuePair(models.Model):
    key = models.CharField(max_length=15)
    value = models.CharField(max_length=50)
    last_updated = models.DateTimeField(default=datetime.now)
    change = models.IntegerField(default=0)

    def __str__(self):
        return "%s: %s" % (self.key, self.value)


class Location(models.Model):
    loc_type = models.CharField(max_length=25)
    longitude = models.FloatField()
    latitude = models.FloatField()
    name = models.CharField(max_length=50)
    alt_names = models.CharField(max_length=250)  # comma separated alternative names
    description = models.CharField(max_length=250, default="", null=True)

    def __str__(self):
        return "%s %s %s" % (self.name, self.latitude, self.longitude)


class Report(models.Model):
    author = models.ForeignKey(Author, on_delete=models.SET_NULL, null=True)
    publication_time = models.DateTimeField()
    pub_link = models.CharField(max_length=250)
    title = models.CharField(max_length=100, null=True)
    longitude = models.FloatField(null=True)
    latitude = models.FloatField(null=True)
    report_type = models.CharField(
        max_length=25, default="Help Needed"
    )  # Relief or Help Needed
    report_subtype = models.CharField(
        max_length=25, default="General"
    )  # Food, Water, Medical Supplies,
    bad_feedback = models.IntegerField(default=0)
    embed_code = models.CharField(max_length=1000)
    resolved = models.BooleanField(default=False)
    dismissed = models.BooleanField(default=False)
    require_review = models.BooleanField(default=False)
    description = models.CharField(max_length=250, null=True, blank=True)
    location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True)

    class Meta:
        unique_together = ["pub_link"]

    def __str__(self):
        return "%s: %s (Requires Review: %s)" % (
            self.author.name,
            self.pub_link,
            self.require_review,
        )

