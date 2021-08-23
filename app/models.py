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


class Institution(models.Model):
    name = models.CharField(max_length=50)
    country = models.CharField(max_length=50)
    website = models.CharField(max_length=50, blank=True, null=True)
    description = models.CharField(max_length=250, blank=True, null=True)
    address = models.CharField(max_length=250, blank=True, null=True)
    twitter_handle = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return "%s [%s]" % (self.name, self.country)


class Location(models.Model):
    loc_type = models.CharField(max_length=25)
    longitude = models.FloatField()
    latitude = models.FloatField()
    name = models.CharField(max_length=50)
    alt_names = models.CharField(max_length=250)  # comma separated alternative names
    description = models.CharField(max_length=250, default="", null=True)

    def __str__(self):
        return "%s %s %s" % (self.name, self.latitude, self.longitude)


class Relief(models.Model):
    PROMISED = "Promised"
    DELIVERED = "Delivered"

    MONEY = "Money"
    FOOD = "Food"
    NECESSITIES = "Necessities"
    PERSONNEL = "Personnel"
    WATER = "Water"
    CONSTRUCTION_MATERIALS = "Construction Materials"
    TEMPORARY_SHELTER = "Temporary Shelter"
    MEDICAL_SUPPLIES = "Medical Supplies"
    MEDICAL_CARE = "Medical care"
    MENTAL_CARE = "Mental Care"
    OTHER = "Other"

    donor = models.ForeignKey(Institution, on_delete=models.SET_NULL, null=True)
    receiver = models.ForeignKey(
        Institution,
        on_delete=models.SET_NULL,
        null=True,
        related_name="receiver_entries",
        blank=True,
    )
    item_type = models.CharField(
        max_length=50,
        choices=[
            (MONEY, "Money"),
            (FOOD, "Food"),
            (NECESSITIES, "Necessities"),
            (PERSONNEL, "Skilled Personnel"),
            (WATER, "Water"),
            (CONSTRUCTION_MATERIALS, "Construction Materials"),
            (TEMPORARY_SHELTER, "Temporary Shelter"),
            (MEDICAL_CARE, "Medical Care"),
            (MEDICAL_SUPPLIES, "Medical Supplies"),
            (MENTAL_CARE, "Mental Care"),
            (OTHER, "Other"),
        ],
    )
    item_subtype = models.CharField(max_length=50, null=True, blank=True)
    quantity = models.IntegerField(default=0)
    unit = models.CharField(max_length=50)
    status = models.CharField(
        max_length=50, choices=[(PROMISED, "Promised"), (DELIVERED, "Delivered")]
    )
    pub_link = models.CharField(max_length=250)
    relief_designation = models.CharField(max_length=500)
    embed_code = models.CharField(max_length=1500, null=True, blank=True)
    target_location = models.ForeignKey(
        Location, on_delete=models.SET_NULL, null=True, blank=True
    )
    donation_date = models.DateTimeField(null=True, default=None)


class Fundraiser(models.Model):
    institution = models.ForeignKey(Institution, on_delete=models.SET_NULL, null=True)
    description = models.CharField(max_length=1500)
    title = models.CharField(max_length=100)
    goal = models.IntegerField(default=0)
    unit = models.CharField(max_length=50)
    status = models.CharField(max_length=50)
    pub_link = models.CharField(max_length=250)
    embed_code = models.CharField(max_length=1500)
    target_location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True)


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
    embed_code = models.CharField(max_length=1500)
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

