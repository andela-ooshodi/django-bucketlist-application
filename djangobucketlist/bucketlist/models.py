from django.db import models
from django.contrib.auth.models import User


class Base(models.Model):
    name = models.CharField(max_length=200)
    date_created = models.DateTimeField('created')
    date_modified = models.DateTimeField('modified')

    class Meta:
        abstract = True


class BucketList(Base):
    author = models.ForeignKey(User)

    class Meta(Base.Meta):
        db_table = 'bucketlist'


class BucketlistItem(Base):
    bucketlist = models.ForeignKey(BucketList)
    done = models.BooleanField()

    class Meta(Base.Meta):
        db_table = 'bucketitem'
