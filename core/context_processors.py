from app.models import KeyValuePair
from django.http import HttpRequest
from decouple import config


def access_site_name(HttpRequest):
    site_name = "Disaster Monitoring"
    site_name_query = KeyValuePair.objects.filter(key="site_name")
    if len(site_name_query) > 0:
        site_name = site_name_query[0].value
    return {
        "site_name": site_name,
        "GOOGLE_ANALYTICS_TAG": config("GOOGLE_ANALYTICS", default=None),
    }
