from __future__ import unicode_literals

from django.db import models


class Timestampable(models.Model):

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Visibility(models.Model):

    PUBLIC = 'public'
    PRIVATE = 'private'

    VISIBILITY_CHOICES = (
        (PUBLIC, PUBLIC),
        (PRIVATE, PRIVATE),
    )

    visibility = models.CharField(max_length=16, choices=VISIBILITY_CHOICES)

    class Meta:
        abstract = True


class Deletable(models.Model):

    deleted = models.DateTimeField(null=True)

    class Meta:
        abstract = True
