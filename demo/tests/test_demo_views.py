from django.test import TestCase
from django.core.urlresolvers import reverse

from ..models import Person


class HomeTest(TestCase):

    def test_get(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('form', response.context)
        form = response.context['form']
        self.assertIn('search_color', form.fields)
        self.assertIn('search_person', form.fields)
        # Color
        search_color = form.fields['search_color']
        attrs_color = search_color.widget.build_attrs()
        self.assertIn('data-url', attrs_color)
        url_color = attrs_color['data-url']
        self.assertEqual(
            url_color,
            reverse('agnocomplete:agnocomplete', args=['AutocompleteColor']))
        # Person
        search_person = form.fields['search_person']
        attrs_person = search_person.widget.build_attrs()
        self.assertIn('data-url', attrs_person)
        url_person = attrs_person['data-url']
        self.assertEqual(
            url_person,
            reverse('agnocomplete:agnocomplete', args=['AutocompletePerson']))

    def test_queries(self):
        # This view should not trigger any SQL query
        # It has no selected value
        with self.assertNumQueries(0):
            self.client.get(reverse('home'))


class FilledFormTest(TestCase):

    def setUp(self):
        super(FilledFormTest, self).setUp()
        self.alice1 = Person.objects.get(pk=1)

    def test_queries(self):
        # This view should just trigger TWO queries
        # It has ONE selected value
        # 1. The first one is to fetch the selected value and check if it's
        #    valid the query is a Model.objects.get(pk=pk)
        # 2. The other is the query that fetches the selected values and feed
        #    the rendered input
        with self.assertNumQueries(2):
            self.client.get(reverse('filled-form'))

    def test_selected(self):
        response = self.client.get(reverse('filled-form'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('form', response.context)
        form = response.context['form']
        self.assertTrue(form.is_valid())
        cleaned_data = form.cleaned_data
        self.assertEquals(
            cleaned_data, {
                "search_color": "grey",
                "search_person": self.alice1
            }
        )
