# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import serializers

from accounts.serializers import BaseUserSerializer

from .models import Post, Partial


class PartialSerializer(serializers.ModelSerializer):

    class Meta:
        model = Partial
        fields = (
            'id', 'object_type'
        )


class PostSerializer(serializers.ModelSerializer):

    user = BaseUserSerializer(read_only=True)

    class Meta:
        model = Post
        fields = (
            'id', 'user', 'visibility', 'partials',
        )

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super(PostSerializer, self).create(validated_data)
