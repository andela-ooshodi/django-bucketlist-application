# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bucketlist', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bucketlist',
            name='date_created',
            field=models.DateTimeField(auto_now_add=True, verbose_name=b'created'),
        ),
        migrations.AlterField(
            model_name='bucketlist',
            name='date_modified',
            field=models.DateTimeField(auto_now=True, verbose_name=b'modified'),
        ),
        migrations.AlterField(
            model_name='bucketlistitem',
            name='date_created',
            field=models.DateTimeField(auto_now_add=True, verbose_name=b'created'),
        ),
        migrations.AlterField(
            model_name='bucketlistitem',
            name='date_modified',
            field=models.DateTimeField(auto_now=True, verbose_name=b'modified'),
        ),
    ]
