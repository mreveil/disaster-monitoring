import datetime
from urllib.parse import urlparse

from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from django.core.validators import URLValidator

from bootstrap_datepicker_plus import DateTimePickerInput


class SubmitReportForm(forms.Form):
    pub_link = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Example: https://twitter.com/Frantzduval/status/1426921202254336002",
                "class": "form-control",
            }
        ),
        help_text="Enter a link to a Facebook, Instagram, Twitter or YouTube post about a need.",
    )

    pub_datetime = forms.DateTimeField(
        widget=DateTimePickerInput(
            # format="%m/%d/%Y %I:%M %p",
            attrs={"placeholder": "Enter the post date and time"},
        ),
        help_text="Enter the date and time when this post was published.).",
    )

    def clean_pub_link(self):
        data = self.cleaned_data["pub_link"]
        host = urlparse(data).hostname
        if not host or not (
            host.endswith(".twitter.com")
            or host.endswith(".facebook.com")
            or host.endswith(".youtube.com")
            or host.endswith(".instagram.com")
        ):
            raise ValidationError(
                _(
                    "Invalid link. Only Twitter, Facebook, Instagram or YouTube posts are supported."
                )
            )

        return data

    def clean_pub_datetime(self):
        data = self.cleaned_data["pub_datetime"]
        # Check if a date is before the earthquake.
        if data < datetime.datetime(2021, 8, 14, 8, 20, tzinfo=datetime.timezone.utc):
            raise ValidationError(_("Invalid date - before the earthquake"))

        # Check if a date is in the allowed range (+4 weeks from today).
        if data > datetime.datetime.now(tz=datetime.timezone.utc):
            raise ValidationError(_("Invalid date - cannot be in the future"))

        return data


class SubmitLinkForm(forms.Form):
    pub_link = forms.CharField(
        validators=[URLValidator()],
        widget=forms.TextInput(
            attrs={"placeholder": "Enter a URL", "class": "form-control",}
        ),
        help_text="Enter a URL.).",
    )
