# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-01-20 07:56
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='rooms',
            fields=[
                ('room_id', models.AutoField(primary_key=True, serialize=False)),
                ('room_name', models.CharField(max_length=60)),
                ('room_size', models.IntegerField()),
                ('room_location', models.TextField()),
                ('room_features', models.TextField()),
                ('in_use', models.BooleanField(default=True)),
            ],
        ),
    ]
