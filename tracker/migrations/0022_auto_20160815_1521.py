# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-08-15 12:21
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0021_document'),
    ]

    operations = [
        migrations.CreateModel(
            name='DocumentCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category_name', models.CharField(max_length=50)),
            ],
        ),
        migrations.RemoveField(
            model_name='document',
            name='department_category',
        ),
        migrations.AddField(
            model_name='document',
            name='document_category',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to='tracker.DocumentCategory'),
            preserve_default=False,
        ),
    ]