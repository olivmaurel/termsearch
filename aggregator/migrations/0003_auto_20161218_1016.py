# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-12-18 10:16
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('aggregator', '0002_auto_20161217_1925'),
    ]

    operations = [
        migrations.RenameField(
            model_name='search',
            old_name='domain',
            new_name='domains',
        ),
    ]
