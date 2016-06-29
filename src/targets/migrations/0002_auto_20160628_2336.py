# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-06-28 15:36
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('targets', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='goal',
            name='completed_on',
            field=models.DateTimeField(blank=True, default=None, null=True),
        ),
        migrations.AddField(
            model_name='milestone',
            name='completed_on',
            field=models.DateTimeField(blank=True, default=None, null=True),
        ),
        migrations.AddField(
            model_name='target',
            name='completed_on',
            field=models.DateTimeField(blank=True, default=None, null=True),
        ),
    ]