# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import routers

from django.conf.urls import url

from .views import (
    LoginView, RegisterView, UserViewSet, FriendsView, FacebookLoginView
)


router = routers.DefaultRouter()
router.register(r'users', UserViewSet)

urlpatterns = router.urls + [
    url(r'^register/$', RegisterView.as_view(), name='register'),
    url(r'^login/$', LoginView.as_view(), name='login'),
    url(r'^friends/$', FriendsView.as_view(), name='friends'),
    url(r'^fb-login/$', FacebookLoginView.as_view(), name='fb-login'),
]
