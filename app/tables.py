import django_tables2 as djtables
from app.models import Report


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

