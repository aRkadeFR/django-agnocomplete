from django.db import models
from .common import COLORS


class Person(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)

    def __unicode__(self):
        return " ".join((self.first_name, self.last_name))
    __str__ = __unicode__

    @property
    def is_active(self):
        # Property needed by the authentication backend
        return True

    def save(self, *args, **kwargs):
        # Last login is a Django User model specific field,
        # no need to handle it
        if "update_fields" in kwargs:
            if 'last_login' in kwargs['update_fields']:
                kwargs['update_fields'].remove('last_login')
        return super(Person, self).save(*args, **kwargs)


class FavoriteColor(models.Model):
    person = models.ForeignKey(Person)
    color = models.CharField(max_length=100, choices=COLORS)

    def __unicode__(self):
        return "{}'s favorite color is {}".format(self.person, self.color)
    __str__ = __unicode__


class Friendship(models.Model):
    person = models.ForeignKey(Person, related_name="person")
    friends = models.ManyToManyField(Person, related_name="friend")

    def __unicode__(self):
        return u"{} is friend with {}".format(
            self.person,
            u", ".join([unicode(f) for f in self.friends.all()]) or u"Nobody"
        )
    __str__ = __unicode__
