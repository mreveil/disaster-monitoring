from django.contrib.auth.models import User, Group
from rest_framework import serializers, viewsets
from .models import Report, Author


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ["url", "username", "email", "groups"]


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ["url", "name"]


class AuthorSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Author
        fields = [
            "name",
            "affiliation",
            "profile_link",
            "affiliation_link",
        ]


class ReportSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Report
        fields = [
            "author",
            "publication_time",
            "pub_link",
            "title",
            "longitude",
            "latitude",
            "bad_feedback",
            "report_type",
            "embed_code",
        ]
