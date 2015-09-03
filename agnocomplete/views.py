import json
from django.http import HttpResponse, Http404
from django.views.generic import View
from django.utils.functional import cached_property
from .register import get_autocomplete_registry


class JSONView(View):

    @property
    def content_type(self):
        """
        Return content-type of the response.
        For a JSONResponseMixin, the obvious answer is ``application/json``.
        But Internet Explorer v8 can't handle this content-type and instead
        of processing it as a normal AJAX data response, it tries to download
        it.
        We're tricking this behaviour by sending back a ``text/html``
        content-type header instead.
        """
        if 'HTTP_X_REQUESTED_WITH' in self.request.META:
            return "application/json;charset UTF-8"
        else:
            return "text/html"

    def get_dataset(self):
        raise NotImplementedError("You must implement a `get_dataset` method")

    def get(self, *args, **kwargs):
        return HttpResponse(
            json.dumps({'data': self.get_dataset()}),
            content_type=self.content_type,
        )


class RegistryMixin(object):

    @cached_property
    def registry(self):
        return get_autocomplete_registry()


class CatalogView(RegistryMixin, JSONView):
    def get_dataset(self):
        return tuple(self.registry.keys())


class AutocompleteView(RegistryMixin, JSONView):

    def get_dataset(self):
        klass_name = self.kwargs.get('klass', None)
        klass = self.registry.get(klass_name, None)
        if not klass:
            raise Http404("Unknown autocomplete `{}`".format(klass_name))
        query = self.kwargs.get('q', "")
        if not query:
            # Empty dict, no value to complete
            return {}