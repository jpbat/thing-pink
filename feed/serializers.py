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

    def to_internal_value(self, data):
        instance_id = data.get('id')
        data = super(PartialSerializer, self).to_internal_value(data)
        data['id'] = instance_id
        return data

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
        """Create and update had to be rewritten.

        Since we are submitting nested instances in the body, we need
        to specify how to deal with the nested items.
        """
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

    def update(self, instance, validated_data):
        """Create and update had to be rewritten.

        Since we are submitting nested instances in the body, we need
        to specify how to deal with the nested items.
        """
        partials = validated_data.pop('partials')
        instance = super(PostSerializer, self).update(instance, validated_data)

        ctx = self.context
        ctx['post'] = instance

        partial_ids = []

        for partial in partials:
            partial_id = partial.get('id')
            if partial_id:
                partial_instance = Partial.objects.get(id=partial_id)
                partial_serializer = PartialSerializer(
                    partial_instance, data=partial, context=ctx
                )
            else:
                partial_serializer = PartialSerializer(
                    data=partial, context=ctx
                )

            partial_serializer.is_valid(raise_exception=True)
            partial_instance = partial_serializer.save()
            partial_ids.append(partial_instance.id)

        # remove the old ugly partials
        instance.partials.exclude(id__in=partial_ids).delete()

        return instance
