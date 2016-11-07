# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from datetime import datetime
from rest_framework.authtoken.models import Token

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models
from django.utils import timezone

from utils.models import Timestampable


class UserManager(BaseUserManager):

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


class User(AbstractBaseUser, Timestampable):

    name = models.CharField(max_length=128)
    username = models.CharField(max_length=32, unique=True)

    objects = UserManager()

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