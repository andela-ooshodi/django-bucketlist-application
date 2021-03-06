"""
Models for bucketlist app
"""

from django.db import models
from django.contrib.auth.models import User


class Base(models.Model):
    name = models.CharField(max_length=200)
    date_created = models.DateTimeField(
        auto_now_add=True, verbose_name='created')
    date_modified = models.DateTimeField(
        auto_now=True, verbose_name='modified')

    class Meta:
        abstract = True
        ordering = ['-date_modified']


class BucketList(Base):
    author = models.ForeignKey(User, related_name='buckets')

    class Meta(Base.Meta):
        db_table = 'bucketlist'


class BucketlistItem(Base):
    bucketlist = models.ForeignKey(BucketList, related_name='bucketitems')
    done = models.BooleanField(default=False)

    class Meta(Base.Meta):
        db_table = 'bucketitem'
        ordering = ['done', '-date_modified']
