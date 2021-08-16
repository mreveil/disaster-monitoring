# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""
import json

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.template import loader
from django.http import HttpResponse
from django import template
from django.contrib.auth.models import User, Group
from django.core import serializers

from rest_framework import viewsets, permissions
from decouple import config

from app.serializers import (
    UserSerializer,
    GroupSerializer,
    ReportSerializer,
    AuthorSerializer,
)
from app.models import Report, Author


# @login_required(login_url="/login/")
def index(request):

    context = {}
    context["segment"] = "index"
    json_serializer = serializers.get_serializer("json")()
    reports = json_serializer.serialize(Report.objects.all(), ensure_ascii=False)

    context = {}
    context["data"] = reports
    context["GOOGLE_MAPS_API_KEY"] = config("GOOGLE_MAPS_API_KEY")
    html_template = loader.get_template("index.html")
    return HttpResponse(html_template.render(context, request))


# @login_required(login_url="/login/")
def pages(request):
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.

    context = {}

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

