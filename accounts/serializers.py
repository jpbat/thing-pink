# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import serializers
from rest_framework.authtoken.serializers import AuthTokenSerializer

from django.contrib.auth import password_validation

from utils.third_party import Facebook

from .models import User, Friendship, FacebookUser


class BaseUserSerializer(serializers.ModelSerializer):
    """This is the base serializer for every user action."""

    password = serializers.CharField(write_only=True)
    token = serializers.CharField(read_only=True)

    class Meta:
        model = User
        fields = (
            'id', 'name', 'username', 'token', 'password'
        )

    def validate_password(self, data):
        password_validation.validate_password(data)
        return data

    def validate(self, data):
        user = self.context['request'].user
        if user.id and user != self.instance:
            raise serializers.ValidationError(
                "You can only change data on your profile"
            )
        return data

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        if password:
            instance.set_password(password)
        return super(BaseUserSerializer, self).update(instance, validated_data)


class RegisterUserSerializer(BaseUserSerializer):
    """This is the serializer used to register a new account."""

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            name=validated_data['name'],
        )
        user.set_password(validated_data['password'])
        user.save()
        user.get_token()
        return user


class LoginUserSerializer(AuthTokenSerializer, BaseUserSerializer):
    """This is the serializer used to login."""

    name = serializers.CharField(required=False)

    def create(self, validated_data):
        user = validated_data['user']
        user.get_token()
        return user


class FriendshipSerializer(serializers.ModelSerializer):
    """This is the serializer used to create and list friendships."""

    friends_since = serializers.DateTimeField(source='created', read_only=True)
    user1 = BaseUserSerializer(read_only=True)
    user2 = BaseUserSerializer(read_only=True)

    class Meta:
        model = Friendship
        fields = (
            'user1', 'user2', 'friends_since'
        )

    def validate(self, validated_data):
        data = self.initial_data
        user1 = data['user1']
        user2 = data['user2']

        if user1 == user2:
            raise serializers.ValidationError(
                'Cannot become friends with yourself.'
            )

        if Friendship.objects.between(user1, user2).exists():
            raise serializers.ValidationError(
                'There is already a friendship between those users.'
            )
        return data


class FacebookLoginUserSerializer(serializers.Serializer):
    """This is the serializer used to login using facebook."""

    access_token = serializers.CharField()

    def create(self, validated_data):
        access_token = validated_data['access_token']

        # try to map directly between access_token and user
        try:
            fb_user = FacebookUser.objects.get(access_token=access_token)
        except FacebookUser.DoesNotExist:
            fb_user = None

        if fb_user:
            user = fb_user.user
            user.get_token()
            return BaseUserSerializer(user).data

        facebook_data = Facebook.get_user_info(access_token=access_token)

        if facebook_data is None:
            return {}

        # check if this facebook account already exists in bd
        try:
            fb_user = FacebookUser.objects.get(facebook_id=facebook_data['id'])
            fb_user.access_token = access_token
            fb_user.save()
        except FacebookUser.DoesNotExist:
            fb_user = None

        if fb_user:
            user = fb_user.user
        else:
            user, _ = User.objects.get_or_create(
                username=facebook_data['id'],
                defaults={
                    'name': facebook_data['name'],
                }
            )
            FacebookUser.objects.create(
                facebook_id=facebook_data['id'],
                access_token=access_token,
                user=user
            )
        user.get_token()
        return BaseUserSerializer(user).data
