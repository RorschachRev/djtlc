# -*- coding: utf-8 -*-
# Generated by Django 1.11.12 on 2018-05-09 16:35
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loan', '0008_loan_data_borrower_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='loan_data',
            name='borrower_type',
            field=models.IntegerField(choices=[(0, 'Individual'), (1, 'Married Couple'), (2, 'Partnership'), (3, 'Corporation'), (4, 'Limited Liability Company'), (5, 'Trust'), (6, 'Investment Group'), (7, 'Other')], default=0),
        ),
    ]