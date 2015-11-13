# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('bucketlist', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bucketlist',
            name='author',
            field=models.ForeignKey(related_name='buckets', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='bucketlistitem',
            name='bucketlist',
            field=models.ForeignKey(related_name='bucketitems', to='bucketlist.BucketList'),
        ),
    ]
