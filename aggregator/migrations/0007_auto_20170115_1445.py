# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-01-15 14:45
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aggregator', '0006_auto_20170115_1442'),
    ]

    operations = [
        migrations.AlterField(
            model_name='website',
            name='name',
            field=models.CharField(max_length=50, unique=True),
        ),
    ]
