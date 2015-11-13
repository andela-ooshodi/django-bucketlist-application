from rest_framework import serializers
from bucketlist.models import BucketList, BucketlistItem


class BucketListSerializer(serializers.ModelSerializer):

    bucketitems = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='name'
    )

    class Meta:
        model = BucketList
        fields = (
            'id', 'name', 'author', 'date_created',
            'date_modified', 'bucketitems')


class BucketItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = BucketlistItem
        fields = (
            'id', 'name', 'bucketlist', 'date_created', 'date_modified', 'done'
        )
