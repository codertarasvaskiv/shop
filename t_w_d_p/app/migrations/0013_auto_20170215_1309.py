# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-15 11:09
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0012_auto_20161201_1959'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='productLogo',
            field=models.FileField(blank=True, upload_to='product_images'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='userLogo',
            field=models.ImageField(blank=True, upload_to='user_images'),
        ),
    ]