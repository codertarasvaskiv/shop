# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-10-21 10:54
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rango', '0004_auto_20161019_1040'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='usage',
            new_name='category',
        ),
        migrations.AlterField(
            model_name='product',
            name='product_logo',
            field=models.FileField(blank=True, upload_to=b'product_images'),
        ),
    ]
