# -*- coding: utf-8 -*-
# Generated by Django 1.11.12 on 2018-05-11 21:07
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('loan', '0013_testmodel_testmodel2'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='testmodel2',
            name='name',
        ),
        migrations.DeleteModel(
            name='TestModel',
        ),
        migrations.DeleteModel(
            name='TestModel2',
        ),
    ]
