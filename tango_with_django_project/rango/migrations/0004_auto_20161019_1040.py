# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-10-19 10:40
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rango', '0003_auto_20161016_0735'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='product_logo',
            field=models.ImageField(blank=True, upload_to=b'product_images'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='user_logo',
            field=models.ImageField(blank=True, upload_to=b'user_images'),
        ),
    ]
