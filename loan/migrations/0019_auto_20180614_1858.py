# -*- coding: utf-8 -*-
# Generated by Django 1.11.12 on 2018-06-14 18:58
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('loan', '0018_auto_20180521_1736'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='loan_workflow',
            name='loan_data',
        ),
        migrations.RemoveField(
            model_name='loan_workflow',
            name='loan_officer',
        ),
        migrations.DeleteModel(
            name='Loan_Workflow',
        ),
    ]