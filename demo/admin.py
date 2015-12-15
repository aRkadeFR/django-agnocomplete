from django.contrib import admin
from django import forms

from agnocomplete import fields

from .models import Person, FavoriteColor, Friendship


class PersonAdmin(admin.ModelAdmin):
    pass


# Autocomplete for FavoriteColor admin
class FavoriteColorModelForm(forms.ModelForm):
    person = fields.AgnocompleteModelField('AutocompletePerson')

    class Meta:
        fields = ('color', 'person')
        model = FavoriteColor


class FavoriteColorAdmin(admin.ModelAdmin):
    form = FavoriteColorModelForm

    class Media:
        css = {
            'screen': ('css/admin.css', 'css/selectize.css',)
        }
        js = (
            'js/jquery.js',
            'js/selectize.js',
            'js/demo/selectize.js',
        )


admin.site.register(Person, PersonAdmin)
admin.site.register(FavoriteColor, FavoriteColorAdmin)
admin.site.register(Friendship)
