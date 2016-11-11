from rest_framework import status
from rest_framework.decorators import detail_route
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from accounts.models import User
from thing_pink.api import APICommonMixin

from .models import Friendship

from .serializers import (
    LoginUserSerializer, RegisterUserSerializer, BaseUserSerializer,
    FriendshipSerializer, FacebookLoginUserSerializer
)


"""
Since a lot of the account actions use the same HTTP Method (POST)
it is needed to separate them in several views.

RegisterView - creates a new user for the system
LoginView - logins with given username and password
UserViewSet - a viewset is a class that provides a lot of tools, update,
    listing etc. With this it makes it a lot easier to create a REST interface.
FriendsView - Returns the list of friends for the authenticated user
FacebookLoginView - The view that deals with the Facebook authentication
"""


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

    @detail_route(methods=[u'post', u'delete'])
    def friend(self, request, *args, **kwargs):
        data = {
            'user1': request.user,
            'user2': self.get_object(),
        }

        if request.method == 'DELETE':
            instance = Friendship.objects.between(
                request.user, self.get_object()
            )
            self.perform_destroy(instance)
            return Response(status=status.HTTP_204_NO_CONTENT)

        serializer = FriendshipSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )


class FriendsView(APICommonMixin, ListAPIView):

    serializer_class = BaseUserSerializer

    def get_queryset(self):
        return User.objects.friends_with(self.request.user)


class FacebookLoginView(APICommonMixin, CreateAPIView):
    serializer_class = FacebookLoginUserSerializer
    authentication_classes = []
    permission_classes = []

    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        if user:
            return Response(user)
        else:
            return Response(
                {'error': 'invalid token'}, status=status.HTTP_400_BAD_REQUEST
            )
