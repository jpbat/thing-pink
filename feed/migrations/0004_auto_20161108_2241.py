# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-11-08 22:41
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('feed', '0003_auto_20161108_2112'),
    ]

    operations = [
        migrations.CreateModel(
            name='Attachment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to='attachments/')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='partial',
            name='text',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='attachment',
            name='partial',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='attachment', to='feed.Partial'),
        ),
    ]
