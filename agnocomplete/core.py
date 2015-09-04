"""
The different autocomplete classes to be discovered
"""
from copy import copy
from django.db.models import Q
from django.utils.encoding import force_text

from .constants import AUTOCOMPLETE_DEFAULT_PAGESIZE
from .constants import AUTOCOMPLETE_MIN_PAGESIZE
from .constants import AUTOCOMPLETE_MAX_PAGESIZE


class AutocompleteBase(object):
    page_size = AUTOCOMPLETE_DEFAULT_PAGESIZE
    page_size_min = AUTOCOMPLETE_MIN_PAGESIZE
    page_size_max = AUTOCOMPLETE_MAX_PAGESIZE

    def __init__(self, page_size=None):
        page_size = page_size or self.page_size
        if page_size > self.page_size_max or page_size < self.page_size_min:
            page_size = self.page_size
        self._page_size = page_size

    def get_page_size(self):
        return self._page_size

    def items(self, query=None):
        raise NotImplementedError(
            "Developer: Your class needs at least a items() method")


class AutocompleteChoices(AutocompleteBase):
    """
    Example::

        class AutocompleteColor(AutocompleteChoices):
            choices = ['red', 'green', 'blue']
    """
    choices = []

    def items(self, query=None):
        if not query:
            return []
        result = copy(self.choices)
        if query:
            result = tuple(filter(lambda x: x.startswith(query), result))

        result = [dict(value=item, label=item) for item in result]
        return result[:self.get_page_size()]


class AutocompleteModel(AutocompleteBase):
    """

    Example::

        class AutocompletePeople(AutocompleteModel):
            model = People
            fields = ['first_name', 'last_name']
    """

    @property
    def model(self):
        raise NotImplementedError(
            "Integrator: You must have a `model` property")

    @property
    def fields(self):
        raise NotImplementedError(
            "Integrator: You must have a `fields` property")

    def _construct_qs_filter(self, field_name):
        """
        Using a field name optionnaly prefixed by `^`, `=`, `@`, return a
        case-insensitive filter condition name usable as a queryset `filter()`
        keyword argument.
        """
        if field_name.startswith('^'):
            return "%s__istartswith" % field_name[1:]
        elif field_name.startswith('='):
            return "%s__iexact" % field_name[1:]
        elif field_name.startswith('@'):
            return "%s__search" % field_name[1:]
        else:
            return "%s__icontains" % field_name

    def get_model_queryset(self):
        return self.model.objects.all()

    def get_queryset(self, query=None):
        """
        Return the filtered queryset
        """
        # Cut this, we don't need no empty query
        if not query:
            return self.model.objects.none()

        qs = self.get_model_queryset()
        conditions = Q()
        for field_name in self.fields:
            conditions |= Q(**{
                self._construct_qs_filter(field_name): query
            })
        qs = qs.filter(conditions)
        return qs

    def items(self, query=None):
        """
        Return the items to be sent to the client
        """
        # Cut this, we don't need no empty query
        if not query:
            return self.model.objects.none()
        qs = self.get_queryset(query)
        result = []
        for item in qs:
            result.append({
                "value": force_text(item.pk),
                "label": force_text(item)
            })
        return result
