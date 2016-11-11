# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from datetime import datetime
from rest_framework.authtoken.models import Token

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models
from django.utils import timezone

from utils.models import Timestampable


class UserManager(BaseUserManager):
    """This manager needs to be implemented, per django requisite."""

    def _create_user(self, username, password, is_staff, is_superuser,
                     **extra_fields):
        """Create User with the given username and password."""
        now = timezone.now()
        user = self.model(
            username=username, is_staff=is_staff, is_active=True,
            is_superuser=is_superuser, last_login=now, date_joined=now,
            **extra_fields
        )
        user.set_password(password)
        user.save()
        return user

    def create_user(self, username, password=None, **extra_fields):
        return self._create_user(username, password, False, False,
                                 **extra_fields)

    def create_superuser(self, username, password, **extra_fields):
        return self._create_user(username, password, True, True,
                                 **extra_fields)


class UserQuerySet(models.QuerySet):

    def friends_with(self, user):
        friend_ids = []

        qs = Friendship.objects.for_user(user)
        for friendship in qs:
            if friendship.user1.id == user.id:
                friend_ids.append(friendship.user2.id)
            else:
                friend_ids.append(friendship.user1.id)

        return self.filter(id__in=friend_ids)


class User(AbstractBaseUser, Timestampable):
    """This class represents the user inside the application."""

    name = models.CharField(max_length=128)
    username = models.CharField(max_length=32, unique=True)

    objects = UserManager.from_queryset(UserQuerySet)()

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    USERNAME_FIELD = 'username'

    def __unicode__(self):
        """Return a combination of name and username."""
        return "{} - {}".format(self.name, self.username)

    def get_token(self):
        """Add this so we can always update the last_login field."""
        self.token, _ = Token.objects.get_or_create(user=self)
        self.last_login = datetime.now()
        self.save()


class FriendshipQuerySet(models.QuerySet):

    def between(self, user1, user2):
        return self.filter(
            models.Q(user1=user1, user2=user2) |
            models.Q(user1=user2, user2=user1)
        )

    def for_user(self, user):
        return self.filter(
            models.Q(user1=user) | models.Q(user2=user)
        )


class Friendship(Timestampable):
    """This class represents a friendship between two users."""

    user1 = models.ForeignKey(User, related_name='added')
    user2 = models.ForeignKey(User, related_name='was_added_by')

    objects = FriendshipQuerySet.as_manager()

    def __unicode__(self):
        """Return a combination of the names from both users."""
        return "{} - {}".format(self.user1.name, self.user2.name)


class FacebookUser(Timestampable):
    """This class represents a facebook profile."""

    facebook_id = models.CharField(max_length=64)
    access_token = models.CharField(max_length=512, null=True)
    user = models.ForeignKey(User)
