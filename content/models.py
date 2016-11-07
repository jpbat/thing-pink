from __future__ import unicode_literals

from accounts.models import User

from django.db import models

from utils.models import Timestampable


class Post(Timestampable):

    user = models.ForeignKey(User, related_name='posts')

    class Meta:
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'

    def __unicode__(self):
        return "{} - {}".format(self.id, self.user.name)


class Partial(Timestampable):

    TYPE_CHOICES = (
        ('image', 'image'),
        ('text', 'text'),
        ('video', 'video'),
        ('post', 'post'),
    )

    post = models.ForeignKey(Post, related_name='partials')
    object_type = models.CharField(max_length=16, choices=TYPE_CHOICES)

    class Meta:
        verbose_name = 'Partial'
        verbose_name_plural = 'Partials'

    def __unicode__(self):
        return self.id
