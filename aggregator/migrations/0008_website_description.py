# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-01-28 18:49
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aggregator', '0007_auto_20170115_1445'),
    ]

    operations = [
        migrations.AddField(
            model_name='website',
            name='description',
            field=models.TextField(default='Enter description'),
        ),
    ]
