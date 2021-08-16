import datetime

from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

from bootstrap_datepicker_plus import DateTimePickerInput


class SubmitReportForm(forms.Form):
    pub_link = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "e.g. https://twitter.com/Frantzduval/status/1426921202254336002",
                "class": "form-control",
            }
        ),
        help_text="Enter a link to a tweet about a need.).",
    )

    pub_datetime = forms.DateTimeField(
        widget=DateTimePickerInput(
            attrs={"placeholder": "Enter the tweet date and time"}
        ),
        help_text="Enter the date and time when this tweet was published.).",
    )

    def clean_pub_link(self):
        data = self.cleaned_data["pub_link"]

        if "twitter.com" not in data:
            print("Error found")
            raise ValidationError(
                _("Invalid link. Only tweets can be reported for now.")
            )

        return data

    def clean_pub_datetime(self):
        data = self.cleaned_data["pub_datetime"]

        # Check if a date is before the earthquake.
        if data < datetime.datetime(2021, 8, 14, 12, 20, tzinfo=datetime.timezone.utc):
            raise ValidationError(_("Invalid date - before the earthquake"))

        # Check if a date is in the allowed range (+4 weeks from today).
        if data > datetime.datetime.now(tz=datetime.timezone.utc):
            raise ValidationError(_("Invalid date - cannot be in the future"))

        return data
