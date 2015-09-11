"""
Demo URL Configuration
"""
from django.conf.urls import include, url
from django.contrib import admin
from agnocomplete import get_namespace

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),

    # Autodiscovered URLs
    url(
        r'^agnocomplete/',
        include(
            'agnocomplete.urls',
            namespace=get_namespace()
        )
    ),

    # Agnocomplete Custom view
    url(r'^hidden-autocomplete/$', 'demo.views.hidden_autocomplete',
        name='hidden-autocomplete'),

    # Templated DEMO views
    url(r'^$', 'demo.views.index', name='home'),
    url(r'^selectize/$', 'demo.views.selectize', name='selectize'),
    url(r'^filled-form/$', 'demo.views.filled_form', name='filled-form'),
    url(r'^search-context/$', 'demo.views.search_context', name='search-context'),  # noqa
    url(r'^custom/$', 'demo.views.search_custom', name='search-custom'),
]
