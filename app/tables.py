import django_tables2 as djtables
from django_filters.views import FilterView
from django_tables2.views import SingleTableMixin

from app.models import Report, Relief, Fundraiser
from app.filters import ReliefFilter


class ReportTable(djtables.Table):
    id = djtables.Column(
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


class ReliefTable(djtables.Table):
    id = djtables.Column(
        attrs={"th": {"scope": "col", "class": "sort"}, "td": {"class": "my-class"},}
    )
    # age = tables.Column()

    class Meta:
        model = Relief
        exclude = (
            "id",
            "embed_code",
            
        )
        attrs = {
            "class": "table align-items-center ",
            "thead": {"class": "thead-light"},
            "tbody": {"class": "list"},
        }
        template_name = "includes/table.html"

class FundraiserTable(djtables.Table):
    id = djtables.Column(
        attrs={"th": {"scope": "col", "class": "sort"}, "td": {"class": "my-class"},}
    )
    # age = tables.Column()
    view_fundraiser = djtables.TemplateColumn('<a href="{{record.pub_link}}">View Fundraiser</a>')
    class Meta:
        model = Fundraiser
        exclude = (
            "id",
            "embed_code",
            "pub_link",
        )
        attrs = {
            "class": "table align-items-center ",
            "thead": {"class": "thead-light"},
            "tbody": {"class": "list"},
        }
        template_name = "includes/table.html"


class FilteredReliefListView(SingleTableMixin, FilterView):
    table_class = ReliefTable
    model = Relief
    template_name = "includes/table.html"

    filterset_class = ReliefFilter
