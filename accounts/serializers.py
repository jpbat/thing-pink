# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import serializers
from rest_framework.authtoken.serializers import AuthTokenSerializer

from django.contrib.auth import password_validation

from .models import User, Friendship


class BaseUserSerializer(serializers.ModelSerializer):

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

    name = serializers.CharField(required=False)

    def create(self, validated_data):
        user = validated_data['user']
        user.get_token()
        return user


class FriendshipSerializer(serializers.ModelSerializer):

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
