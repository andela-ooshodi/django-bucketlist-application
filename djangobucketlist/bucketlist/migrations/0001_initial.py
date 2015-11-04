# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='BucketList',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
                ('date_created', models.DateTimeField(verbose_name=b'created')),
                ('date_modified', models.DateTimeField(verbose_name=b'modified')),
                ('author', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
                'db_table': 'bucketlist',
            },
        ),
        migrations.CreateModel(
            name='BucketlistItem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
                ('date_created', models.DateTimeField(verbose_name=b'created')),
                ('date_modified', models.DateTimeField(verbose_name=b'modified')),
                ('done', models.BooleanField()),
                ('bucketlist', models.ForeignKey(to='bucketlist.BucketList')),
            ],
            options={
                'abstract': False,
                'db_table': 'bucketitem',
            },
        ),
    ]
