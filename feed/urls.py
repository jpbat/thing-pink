# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import routers

from django.conf.urls import url

from .views import PostViewSet, FeedView

router = routers.DefaultRouter()
router.register(r'posts', PostViewSet)

urlpatterns = router.urls + [
    url(r'^feed/$', FeedView.as_view(), name='feed'),
]
