# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import serializers

from accounts.serializers import BaseUserSerializer

from .models import Post, Partial


class PartialSerializer(serializers.ModelSerializer):

    class Meta:
        model = Partial
        fields = (
            'id', 'object_type', 'text', 'url'
        )

    def create(self, validated_data):
        post = self.context['post']
        validated_data['post'] = post
        return super(PartialSerializer, self). create(validated_data)


class PostSerializer(serializers.ModelSerializer):

    user = BaseUserSerializer(read_only=True)
    partials = PartialSerializer(many=True)

    class Meta:
        model = Post
        fields = (
            'id', 'user', 'visibility', 'partials',
        )

    def validate(self, validated_data):

        if not validated_data.get('partials'):
            raise serializers.ValidationError(
                'At least one partial should be provided.'
            )
        return validated_data

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        partials = validated_data.pop('partials')

        instance = super(PostSerializer, self).create(validated_data)

        ctx = self.context
        ctx['post'] = instance
        partial_serializer = PartialSerializer(
            data=partials, many=True, context=ctx
        )
        partial_serializer.is_valid()
        partial_serializer.save()

        return instance
