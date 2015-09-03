"""
Core autocomplete
"""
from agnocomplete.register import register
from agnocomplete.core import AutocompleteChoices, AutocompleteModel
from demo.models import Person


class AutocompleteChoicesExample(AutocompleteChoices):
    choices = ['green', 'gray', 'blue', 'grey']


class AutocompletePerson(AutocompleteModel):
    model = Person
    fields = ['first_name', 'last_name']


# Registration
register(AutocompleteChoicesExample)
register(AutocompletePerson)
