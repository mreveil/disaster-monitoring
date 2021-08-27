# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""
import json
import requests
import unicodedata
import datetime
from urllib.parse import urlparse

from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect
from django import template
from django.contrib.auth.models import User, Group
from django.core import serializers
from django.db.models import Q
from django.db.utils import IntegrityError

from rest_framework import viewsets, permissions
from decouple import config
import django_tables2 as djtables


from app.serializers import (
    UserSerializer,
    GroupSerializer,
    ReportSerializer,
    AuthorSerializer,
)
from app.models import (
    Report,
    Author,
    KeyValuePair,
    Location,
    MediaCoverage,
    KeyEvent,
    Relief,
    UserSubmission,
)
from app.forms import SubmitReportForm, SubmitLinkForm
from app.tables import ReportTable, ReliefTable, FilteredReliefListView
from app.tweet_processing import process_tweet

# @login_required(login_url="/login/")
def index(request):

    clean_form = False
    context = {}
    context["segment"] = "index"
    json_serializer = serializers.get_serializer("json")()
    reports = Report.objects.filter(
        longitude__isnull=False, dismissed=False, require_review=False
    ).order_by("-publication_time")
    reports_json = json_serializer.serialize(reports, ensure_ascii=False,)
    reports_table = ReportTable(reports)
    djtables.config.RequestConfig(request, paginate={"per_page": 10}).configure(
        reports_table
    )

    for key_value_pair in KeyValuePair.objects.all():
        context[key_value_pair.key + "_value"] = key_value_pair.value
        context[key_value_pair.key + "_last_updated"] = key_value_pair.last_updated
        context[key_value_pair.key + "_change"] = key_value_pair.change

    if request.method == "POST":
        # Create form instance
        form = SubmitReportForm(request.POST)
        clean_form = True

        if form.is_valid():
            pub_link = form.cleaned_data["pub_link"]
            host = urlparse(pub_link).hostname
            if host and host.endswith(".twitter.com"):
                msg, success = process_tweet(
                    pub_link, form.cleaned_data["pub_datetime"]
                )
            else:
                try:
                    UserSubmission.objects.create(
                        pub_link=form.cleaned_data["pub_link"],
                        submission_type=UserSubmission.RELIEF,
                        publication_datetime=form.cleaned_data["pub_datetime"],
                    )
                    success = True
                    msg = "Thanks for your contribution. Your link will be verified and added later."
                except IntegrityError:
                    success = False
                    msg = "Link has already been added. Please add a new one."

            if success:
                messages.success(request, msg)
            else:
                messages.error(request, msg)

        else:
            print("The form is not valid.")
            messages.error(
                request,
                "Invalid link. Only Facebook, Instagram, Twitter and YouTube links are supported.",
            )
    else:
        form = SubmitReportForm()

    context["form"] = form
    context["data"] = reports_json
    context["reports"] = reports
    context["GOOGLE_MAPS_API_KEY"] = config("GOOGLE_MAPS_API_KEY")
    html_template = loader.get_template("index.html")
    if clean_form:
        return HttpResponseRedirect("/")
    return HttpResponse(html_template.render(context, request))


def load_relief_data_context(request):

    context = {}
    load_template = "relief-data.html"

    context["segment"] = load_template

    reliefs = Relief.objects.all().order_by("-publication_date")
    reliefs_table = ReliefTable(reliefs)
    djtables.config.RequestConfig(request, paginate={"per_page": 15}).configure(
        reliefs_table
    )
    context["table"] = reliefs_table
    context["data"] = reliefs

    clean_form = False
    if request.method == "POST":
        # Create form instance
        form = SubmitLinkForm(request.POST)
        clean_form = True

        if form.is_valid():
            try:
                UserSubmission.objects.create(
                    pub_link=form.cleaned_data["pub_link"],
                    submission_type=UserSubmission.RELIEF,
                )
                msg = "Thanks for your contribution. Your link will be verified and added later."
            except IntegrityError:
                msg = "Link has already been added. Please add a new one."

            messages.success(
                request, msg,
            )
        else:
            messages.error(request, "Invalid link. Please try a different one.")
    else:
        form = SubmitReportForm()

    context["form"] = form
    context["clean_form"] = clean_form
    return context


# @login_required(login_url="/login/")
def pages(request):
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.

    context = {}
    try:

        load_template = request.path.split("/")[-1]
        context["segment"] = load_template

        if load_template == "media-coverage.html":
            news_articles = MediaCoverage.objects.all()
            context["articles"] = news_articles

        elif load_template == "timeline.html":
            key_events = KeyEvent.objects.all().order_by("-pub_time")
            context["key_events"] = key_events

        elif load_template == "relief-data.html":
            context.update(load_relief_data_context(request))
            if context["clean_form"]:
                return HttpResponseRedirect("/relief-data.html")

        html_template = loader.get_template(load_template)
        return HttpResponse(html_template.render(context, request))

    except template.TemplateDoesNotExist:

        html_template = loader.get_template("page-404.html")
        return HttpResponse(html_template.render(context, request))

    except:

        html_template = loader.get_template("page-500.html")
        return HttpResponse(html_template.render(context, request))


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """

    queryset = User.objects.all().order_by("-date_joined")
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """

    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]


class ReportViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows reports to be viewed or edited.
    """

    queryset = Report.objects.all()
    serializer_class = ReportSerializer
    permission_classes = [permissions.IsAuthenticated]


class AuthorViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows authors to be viewed or edited.
    """

    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [permissions.IsAuthenticated]

