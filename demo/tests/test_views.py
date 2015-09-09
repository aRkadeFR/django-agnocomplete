# -*- coding: utf8 -*-
import json

from django.core.urlresolvers import reverse
from django.utils.encoding import force_text as text
from django.contrib.auth.models import User

from ..models import Person
from . import RegistryTestGeneric


def get_json(response, key='data'):
    data = json.loads(response.content.decode())
    if key:
        return data.get(key, None)
    return data


class CatalogViewTest(RegistryTestGeneric):

    def test_get(self):
        # FIXME: the namespace should be a settings parameter
        response = self.client.get(reverse('agnocomplete:catalog'))
        data = get_json(response)
        self._test_registry_keys(data)


class AgnocompleteViewTest(RegistryTestGeneric):

    def test_get_404(self):
        # FIXME: the namespace should be a settings parameter
        response = self.client.get(
            reverse('agnocomplete:agnocomplete', args=['MEUH']))
        self.assertEqual(response.status_code, 404)


class AutocompleteViewTestGeneric(object):
    view_key = "PLEASE DEFINE ME"

    def test_url(self):
        # FIXME: the namespace should be a settings parameter
        response = self.client.get(
            reverse('agnocomplete:agnocomplete', args=[self.view_key]))
        self.assertEqual(response.status_code, 200)

    def test_noquery(self):
        response = self.client.get(
            reverse('agnocomplete:agnocomplete', args=[self.view_key]),
        )
        self.assertEqual(response.status_code, 200)
        data = get_json(response)
        # No query, the dataset should be empty
        self.assertFalse(data)

    def test_empty_query(self):
        response = self.client.get(
            reverse('agnocomplete:agnocomplete', args=[self.view_key]),
            data={"q": ""}
        )
        self.assertEqual(response.status_code, 200)
        data = get_json(response)
        # No query, the dataset should be empty
        self.assertFalse(data)


class AutocompletePersonViewTest(AutocompleteViewTestGeneric,
                                 RegistryTestGeneric):
    view_key = 'AutocompletePerson'

    def setUp(self):
        super(AutocompletePersonViewTest, self).setUp()
        self.alice1 = Person.objects.get(pk=1)
        self.alice2 = Person.objects.get(pk=2)
        self.bob = Person.objects.get(pk=3)
        self.alice3 = Person.objects.get(pk=4)
        self.alice4 = Person.objects.get(pk=5)

    def test_autocomplete_person_queries(self):
        response = self.client.get(
            reverse('agnocomplete:agnocomplete', args=[self.view_key]),
            data={"q": "ali"}
        )
        self.assertEqual(response.status_code, 200)
        data = get_json(response)
        # query, the dataset has 4 records
        self.assertTrue(data)
        self.assertEqual(len(data), 4)
        self.assertIn({
            "value": text(self.alice1.pk),
            "label": text(self.alice1)},
            data
        )
        self.assertIn({
            "value": text(self.alice2.pk),
            "label": text(self.alice2)},
            data
        )
        self.assertIn({
            "value": text(self.alice3.pk),
            "label": text(self.alice3)},
            data
        )
        self.assertIn({
            "value": text(self.alice4.pk),
            "label": text(self.alice4)},
            data
        )

    def test_autocomplete_person_paginated(self):
        response = self.client.get(
            reverse('agnocomplete:agnocomplete', args=[self.view_key]),
            data={"q": "ali", "page_size": 3}
        )
        self.assertEqual(response.status_code, 200)
        data = get_json(response)
        # query, the dataset has 4 records
        self.assertTrue(data)
        self.assertEqual(len(data), 3)


class AutocompleteColorViewTest(AutocompleteViewTestGeneric,
                                RegistryTestGeneric):
    view_key = 'AutocompleteColor'


class SearchContextFormTest(AutocompleteViewTestGeneric,
                            RegistryTestGeneric):
    view_key = 'AutocompletePersonDomain'

    def test_search_unauthorized(self):
        url = reverse(
            'agnocomplete:agnocomplete', args=[self.view_key],
        )
        response = self.client.get(url, data={"q": "ali"})
        self.assertEqual(response.status_code, 403)

    def test_authorized_empty(self):
        User.objects.create_user(
            'john', 'lennon@thebeatles.com', 'johnpassword'
        )
        url = reverse(
            'agnocomplete:agnocomplete', args=[self.view_key],
        )
        # Logged in with John
        self.client.login(username='john', password='johnpassword')
        response = self.client.get(url, data={"q": "ali"})
        self.assertEqual(response.status_code, 200)
        data = get_json(response)
        self.assertFalse(data)

    def test_authorized_result(self):
        User.objects.create_user(
            'bob', 'bob@example.com', 'bobpassword'
        )
        url = reverse(
            'agnocomplete:agnocomplete', args=[self.view_key],
        )
        # Logged in with Bob
        self.client.login(username='bob', password='bobpassword')
        response = self.client.get(url, data={"q": "ali"})
        self.assertEqual(response.status_code, 200)
        data = get_json(response)
        self.assertTrue(data)
