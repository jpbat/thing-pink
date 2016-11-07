from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from accounts.models import User
from thing_pink.api import APICommonMixin

from .serializers import (
    LoginUserSerializer, RegisterUserSerializer, BaseUserSerializer
)


class RegisterView(APICommonMixin, CreateAPIView):
    model = User
    allowed_methods = [u'post']
    serializer_class = RegisterUserSerializer
    authentication_classes = []
    permission_classes = []


class LoginView(APICommonMixin, CreateAPIView):
    allowed_methods = [u'post']
    serializer_class = LoginUserSerializer
    authentication_classes = []
    permission_classes = []


class UserViewSet(APICommonMixin, ModelViewSet):
    queryset = User.objects.all()
    serializer_class = BaseUserSerializer

    def create(self, request, *args, **kwargs):
        return Response(
            status=status.HTTP_405_METHOD_NOT_ALLOWED,
            data={
                "detail": "Method \"POST\" not allowed."
            }
        )

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if request.user != instance:
            return Response(status=status.HTTP_404_NOT_FOUND)
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
