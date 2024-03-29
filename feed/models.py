from __future__ import unicode_literals

from django.db import models

from accounts.models import User
from utils.models import Timestampable, Visibility, Deletable


class PostManager(models.Manager):

    def get_queryset(self):
        return super(PostManager, self).get_queryset().filter(
            deleted__isnull=True
        )


class PostQuerySet(models.QuerySet):

    def public(self):
        return self.filter(visibility__iexact=Visibility.PUBLIC)

    def from_user(self, user):
        return self.filter(user=user)

    def feed_for_user(self, user):
        if user.is_anonymous():
            return self.public()

        friend_ids = (
            User.objects.friends_with(user)
            .values_list('id', flat=True)
        )
        return self.filter(user_id__in=friend_ids)


class Post(Timestampable, Visibility, Deletable):
    """This class represents a user post.

    A user post can have multiple partials from different types such as images,
    text or even videos. Each post has a owner which is called user.
    """

    user = models.ForeignKey(User, related_name='posts')

    objects = PostManager.from_queryset(PostQuerySet)()

    class Meta:
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'
        ordering = ['-created']

    def __unicode__(self):
        """Return the id."""
        return "{} - {}".format(self.id, self.user.name)


class Partial(Timestampable):
    """This class represents each partial from a post."""

    TYPE_CHOICES = (
        ('image', 'image'),
        ('text', 'text'),
        ('video', 'video'),
    )

    post = models.ForeignKey(Post, related_name='partials')
    object_type = models.CharField(max_length=16, choices=TYPE_CHOICES)
    text = models.TextField(null=True)

    class Meta:
        verbose_name = 'Partial'
        verbose_name_plural = 'Partials'

    @property
    def url(self):
        return self.attachment.file.filename


class Attachment(Timestampable):
    """This class allows us to upload files to add to our post."""

    partial = models.OneToOneField(
        Partial, related_name='attachment', null=True
    )
    file = models.FileField(upload_to='attachments/')
