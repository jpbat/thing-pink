# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import routers

from django.conf.urls import url

from .views import (
    LoginView, RegisterView, UserViewSet
)


router = routers.DefaultRouter()
router.register(r'users', UserViewSet)

urlpatterns = router.urls + [
    url(r'^register/$', RegisterView.as_view(), name='register'),
    url(r'^login/$', LoginView.as_view(), name='login'),
]
