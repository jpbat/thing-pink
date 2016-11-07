from django.conf import settings

from rest_framework.response import Response
from rest_framework.views import APIView

from .api import APICommonMixin


class AppInfo(APICommonMixin, APIView):

    def get(self, request, format=None):
        return Response(data=settings.API_VERSIONS)
