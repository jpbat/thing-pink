from __future__ import unicode_literals

from django.db import models
from django.utils import timezone


class Timestampable(models.Model):
    """Extend this model to have created and updated timestamps."""

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Visibility(models.Model):
    """Extend this model to have visibility tags."""

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
    """Extend this model to have soft deletable."""

    deleted = models.DateTimeField(null=True)

    class Meta:
        abstract = True

    def delete(self):
        self.deleted = timezone.now()
        self.save()
