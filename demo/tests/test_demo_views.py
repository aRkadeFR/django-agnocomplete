from django.test import TestCase
from django.core.urlresolvers import reverse
try:
    from django.test import override_settings
except ImportError:
    # Django 1.6
    from django.test.utils import override_settings

from agnocomplete import get_namespace
from agnocomplete.views import AgnocompleteJSONView
from ..models import Person


class HomeTest(TestCase):

    def test_widgets(self):
        # This test will validate the widget/field building
        # for all Agnocomplete-ready fields.
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('form', response.context)
        form = response.context['form']
        self.assertIn('search_color', form.fields)
        self.assertIn('search_person', form.fields)
        search_color = form.fields['search_color']
        attrs_color = search_color.widget.build_attrs()
        self.assertIn('data-url', attrs_color)
        self.assertIn('data-query-size', attrs_color)
        self.assertIn('data-agnocomplete', attrs_color)

    @override_settings(AGNOCOMPLETE_DATA_ATTRIBUTE='wow')
    def test_data_attribute(self):
        response = self.client.get(reverse('home'))
        form = response.context['form']
        search_color = form.fields['search_color']
        attrs_color = search_color.widget.build_attrs()
        self.assertIn('data-url', attrs_color)
        self.assertIn('data-query-size', attrs_color)
        self.assertIn('data-wow', attrs_color)

    def test_get(self):
        response = self.client.get(reverse('home'))
        form = response.context['form']
        # Color
        search_color = form.fields['search_color']
        attrs_color = search_color.widget.build_attrs()
        url_color = attrs_color['data-url']
        self.assertEqual(
            url_color,
            reverse(
                get_namespace() + ':agnocomplete',
                args=['AutocompleteColor']
            )
        )
        # Person
        search_person = form.fields['search_person']
        attrs_person = search_person.widget.build_attrs()
        url_person = attrs_person['data-url']
        self.assertEqual(
            url_person,
            reverse(
                get_namespace() + ':agnocomplete',
                args=['AutocompletePerson']
            )
        )

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
        self.assertEqual(
            cleaned_data, {
                "search_color": "grey",
                "search_person": self.alice1
            }
        )


class CustomSearchTest(TestCase):

    def test_widgets(self):
        response = self.client.get(reverse('search-custom'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('form', response.context)
        form = response.context['form']
        self.assertIn('search_color', form.fields)
        search_color = form.fields['search_color']
        attrs_color = search_color.widget.build_attrs()
        self.assertIn('data-url', attrs_color)
        self.assertEqual(
            attrs_color['data-url'],
            reverse('hidden-autocomplete')
        )



class ABCTestView(TestCase):

    def test_AgnocompleteJSONView(self):

        class WickedAgnocompleteJSONView(AgnocompleteJSONView):
            pass

        with self.assertRaises(TypeError) as e:
            WickedAgnocompleteJSONView()
        exception = e.exception.args[0]
        self.assertEqual(
            exception,
            """Can't instantiate abstract class WickedAgnocompleteJSONView\
 with abstract methods get_dataset""")


class JSDemoViews(TestCase):

    def test_selectize(self):
        response = self.client.get(reverse('selectize'))
        self.assertEqual(response.status_code, 200)

    def test_jquery_autocomplete(self):
        response = self.client.get(reverse('jquery-autocomplete'))
        self.assertEqual(response.status_code, 200)
