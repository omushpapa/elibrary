# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-08-07 21:51
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('repo', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='request',
            name='userid',
        ),
        migrations.DeleteModel(
            name='Request',
        ),
    ]