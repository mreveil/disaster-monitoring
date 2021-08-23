import django_filters as df
from app.models import Relief


class ReliefFilter(df.FilterSet):
    class Meta:
        model = Relief
        exclude = (
            "id",
            "embed_code",
            "pub_link",
        )
