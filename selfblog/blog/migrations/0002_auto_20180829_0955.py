# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-08-29 01:55
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='tags',
            field=models.ManyToManyField(related_name='posts', to='blog.Tag', verbose_name='标签'),
        ),
    ]
