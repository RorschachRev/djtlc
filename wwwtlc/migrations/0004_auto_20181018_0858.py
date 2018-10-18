# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2018-10-18 14:58
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wwwtlc', '0003_auto_20180913_1104'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='mortgagedesired',
            name='if_not_listed',
        ),
        migrations.AlterField(
            model_name='address',
            name='country',
            field=models.CharField(default='US', max_length=3),
        ),
        migrations.AlterField(
            model_name='borrowerinforequest',
            name='fico',
            field=models.IntegerField(choices=[(0, '720+'), (1, '690-719'), (2, '660-679'), (3, '630-659'), (4, 'Unknown'), (5, 'Select')], default=5, help_text='(approximate credit score)', verbose_name='FICO'),
        ),
        migrations.AlterField(
            model_name='currentmortgage',
            name='late_payments',
            field=models.IntegerField(choices=[(0, 'No'), (1, 'Yes'), (2, 'Select')], default=2, verbose_name='Have you made any late payments?'),
        ),
        migrations.AlterField(
            model_name='mortgagedesired',
            name='term_desired',
            field=models.IntegerField(choices=[(0, '20 Year'), (1, '15 Year'), (2, '10 Year'), (3, 'Less than 10 Years'), (4, 'Not Listed / Not Sure')], default=0, verbose_name='Desired Term'),
        ),
        migrations.AlterField(
            model_name='propertyinforequest',
            name='property_type',
            field=models.IntegerField(choices=[(0, 'Commercial'), (1, 'Industrial'), (2, 'Residential'), (3, 'Mixed'), (4, 'Select Property Type')], default=4, verbose_name='Property Type'),
        ),
    ]