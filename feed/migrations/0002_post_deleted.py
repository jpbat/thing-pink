# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-11-08 00:01
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('feed', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='deleted',
            field=models.DateTimeField(null=True),
        ),
    ]
