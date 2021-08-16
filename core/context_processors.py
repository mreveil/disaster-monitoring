from app.models import KeyValuePair
from django.http import HttpRequest


def access_site_name(HttpRequest):

    return {"site_name": KeyValuePair.objects.filter(key="site_name")[0].value}
