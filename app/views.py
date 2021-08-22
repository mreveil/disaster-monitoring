# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""
import json
import requests
import unicodedata
import datetime

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
import django_tables2 as tables


from app.serializers import (
    UserSerializer,
    GroupSerializer,
    ReportSerializer,
    AuthorSerializer,
)
from app.models import Report, Author, KeyValuePair, Location, MediaCoverage, KeyEvent
from app.forms import SubmitReportForm

twitter_oembed_url = "https://publish.twitter.com/oembed?url="


def compare_strs(s1, s2):
    def NFD(s):
        return unicodedata.normalize("NFD", s)

    return NFD(s1) in NFD(s2)


def find_matching_locations(text, location_list):
    matching_locations = []
    for loc in location_list:
        if compare_strs(loc.name.casefold(), text.casefold()):
            matching_locations.append(loc)
        else:
            for other_name in loc.alt_names.split(","):
                if compare_strs(other_name.casefold(), text.casefold()):
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

        if city is None and location is None:
            longitude, latitude = None, None
            msg = "Unable to extract a location from this tweet. It is saved for manual review."
            require_review = True
        else:
            if location is not None:  # Use the specific location for long and lat
                longitude = location.longitude
                latitude = location.latitude
            else:
                longitude = city.longitude
                latitude = city.latitude
            msg = "Tweet added successfully"
            require_review = False

        try:
            rep = Report.objects.create(
                author=author,
                publication_time=pub_datetime + datetime.timedelta(hours=4),
                pub_link=pub_link,
                location=city,
                longitude=longitude,
                latitude=latitude,
                report_type="Help Needed",
                report_subtype="General",
                title=None,
                description=None,
                require_review=require_review,
                embed_code=embed_code,
            )
            success = True
        except IntegrityError:
            msg = "Tweet has already been added. Please add a new one."
            success = False

    else:
        msg = "Unable to retrieve this tweet. Please try again later."
    return msg, success


class ReportTable(tables.Table):
    id = tables.Column(
        attrs={"th": {"scope": "col", "class": "sort"}, "td": {"class": "my-class"},}
    )
    # age = tables.Column()

    class Meta:
        model = Report
        attrs = {
            "class": "table align-items-center",
            "thead": {"class": "thead-light"},
            "tbody": {"class": "list"},
        }
        template_name = "includes/table.html"


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
    tables.config.RequestConfig(request, paginate={"per_page": 10}).configure(
        reports_table
    )
    # reports_table.paginate(page=request.GET.get("page", 1), per_page=10)

    for key_value_pair in KeyValuePair.objects.all():
        context[key_value_pair.key + "_value"] = key_value_pair.value
        context[key_value_pair.key + "_last_updated"] = key_value_pair.last_updated
        context[key_value_pair.key + "_change"] = key_value_pair.change

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
        else:
            print("The form is not valid.")
            messages.error(
                request, "Invalid link. Only tweets can be submitted for now."
            )
    else:
        form = SubmitReportForm()

    context["form"] = form
    context["data"] = reports_json
    # context["table"] = reports_table
    context["reports"] = reports
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

        print("segment is:", load_template)

        if load_template == "media-coverage.html":
            news_articles = MediaCoverage.objects.all()
            context["articles"] = news_articles

        if load_template == "timeline.html":
            key_events = KeyEvent.objects.all().order_by("-pub_time")
            context["key_events"] = key_events
            print("Key events are: ", key_events)

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

