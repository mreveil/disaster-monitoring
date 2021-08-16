# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""
import json
import requests

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

from app.serializers import (
    UserSerializer,
    GroupSerializer,
    ReportSerializer,
    AuthorSerializer,
)
from app.models import Report, Author, KeyValuePair, Location
from app.forms import SubmitReportForm

twitter_oembed_url = "https://publish.twitter.com/oembed?url="


def find_matching_locations(text, location_list):
    matching_locations = []
    for loc in location_list:
        if loc.name.lower() in text.lower():
            matching_locations.append(loc)
        else:
            for other_name in loc.alt_names.split(","):
                if other_name.lower() in text.lower():
                    matching_locations.append(loc)
                    break

    # Return the fist match | TODO: Pick one of the locations better
    if len(matching_locations) >= 1:
        return matching_locations[0]
    else:
        return None


def identify_city(tweet_text):
    # Get all locations from database
    locations = Location.objects.filter(loc_type="City")
    # Check which known city is in the tweet
    return find_matching_locations(tweet_text, locations)


def identify_specific_location(tweet_text):
    # Get all locations from database
    locations = Location.objects.filter(~Q(loc_type="City"))
    # Check which known locations are in the tweet
    return find_matching_locations(tweet_text, locations)


def process_tweet(pub_link, pub_datetime):
    r = requests.get(twitter_oembed_url + pub_link)
    success = False
    if r.status_code == 200:
        data = r.json()
        embed_code = data["html"].replace(
            '<script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>',
            "",
        )
        # Add author if not already in list
        author, _ = Author.objects.get_or_create(
            name=data["author_name"], profile_link=data["author_url"]
        )
        city = identify_city(embed_code)
        location = identify_specific_location(embed_code)
        if city is not None:
            print("location pk and name: ", city.pk, city)
            longitude = city.longitude
            latitude = city.latitude
            if location is not None:
                longitude = location.longitude
                latitude = location.latitude
            try:
                rep = Report.objects.create(
                    author=author,
                    publication_time=pub_datetime,
                    pub_link=pub_link,
                    location=city,
                    longitude=longitude,
                    latitude=latitude,
                    report_type="Help Needed",
                    report_subtype="General",
                    title=None,
                    description=None,
                )
                print("Report created: ", rep)
                msg = "Tweet added successfully"
                success = True
            except IntegrityError:
                msg = "Tweet has already been added. Please add a new one."
                print("We are here")
                success = False
        else:  # Ask user to submit coordinates and save with require approval flag
            msg = "Unable to extract a location from this tweet. Please try a different one."

    else:
        msg = "Unable to retrieve this tweet. Please try again later."
    return msg, success


# @login_required(login_url="/login/")
def index(request):

    clean_form = False
    context = {}
    context["segment"] = "index"
    json_serializer = serializers.get_serializer("json")()
    reports = json_serializer.serialize(Report.objects.all(), ensure_ascii=False)

    for key_value_pair in KeyValuePair.objects.all():
        context[key_value_pair.key] = key_value_pair.value

    if request.method == "POST":
        # Create form instance
        form = SubmitReportForm(request.POST)
        clean_form = True
        if form.is_valid():
            msg, success = process_tweet(
                form.cleaned_data["pub_link"], form.cleaned_data["pub_datetime"]
            )
            if success:
                messages.success(request, msg)
            else:
                messages.error(request, msg)
            print("This is the message: ", msg)
        else:
            messages.error(
                request, "Invalid link. Only tweets can be submitted for now."
            )
    else:
        form = SubmitReportForm()

    context["form"] = form
    context["data"] = reports
    context["GOOGLE_MAPS_API_KEY"] = config("GOOGLE_MAPS_API_KEY")
    html_template = loader.get_template("index.html")
    if clean_form:
        return HttpResponseRedirect("/")
    return HttpResponse(html_template.render(context, request))


# @login_required(login_url="/login/")
def pages(request):
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.

    context = {}
    for key_value_pair in KeyValuePair.objects.all():
        context[key_value_pair.key] = key_value_pair.value

    try:

        load_template = request.path.split("/")[-1]
        context["segment"] = load_template

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

