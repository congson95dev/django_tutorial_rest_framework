from django_filters import FilterSet

from snippets.models import Snippet


# custom filter by using https://django-filter.readthedocs.io/en/stable/guide/usage.html
# this library will help us lower the code for the filter
# we can check this by open swagger and go to /snippets
# then click to button "filter" and try to filter
class SnippetFilter(FilterSet):
    class Meta:
        model = Snippet
        fields = {
            'category_id': ['exact'],
            'decimal_field': ['lt', 'gt'],
        }
