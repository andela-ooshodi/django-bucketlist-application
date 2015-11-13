from rest_framework import serializers
from bucketlist.models import BucketList, BucketlistItem
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    buckets = serializers.PrimaryKeyRelatedField(
        many=True, queryset=BucketList.objects.all())

    class Meta:
        model = User
        fields = ('id', 'username', 'buckets')


class BucketListSerializer(serializers.ModelSerializer):

    bucketitems = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    author = serializers.ReadOnlyField(source='author.username')

    class Meta:
        model = BucketList
        fields = (
            'id', 'name', 'author', 'date_created',
            'date_modified', 'bucketitems')


class BucketItemSerializer(serializers.ModelSerializer):

    bucketlist = serializers.ReadOnlyField(source='bucketlist.name')

    class Meta:
        model = BucketlistItem
        fields = (
            'id', 'name', 'bucketlist', 'date_created', 'date_modified', 'done'
        )
