# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-16 09:09
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0014_auto_20170215_1527'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='brand',
        ),
        migrations.AddField(
            model_name='product',
            name='description',
            field=models.CharField(default=32, max_length=300),
            preserve_default=False,
        ),
    ]
