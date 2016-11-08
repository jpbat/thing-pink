# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import routers

from .views import PostViewSet


router = routers.DefaultRouter()
router.register(r'posts', PostViewSet)

urlpatterns = router.urls
