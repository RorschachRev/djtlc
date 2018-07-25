# -*- coding: utf-8 -*-
# Generated by Django 1.11.12 on 2018-07-25 19:33
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('wwwtlc', '0004_auto_20180724_2130'),
    ]

    operations = [
        migrations.AlterField(
            model_name='borrowerinforequest',
            name='language',
            field=models.CharField(blank=True, default='en-us', max_length=8, null=True),
        ),
        migrations.AlterField(
            model_name='borrowerinforequest',
            name='type',
            field=models.IntegerField(choices=[(0, 'Business'), (1, 'Personal')], default=0, verbose_name='Type'),
        ),
        migrations.AlterField(
            model_name='currentmortgage',
            name='current_loan_type',
            field=models.IntegerField(choices=[(0, 'Fixed'), (1, 'ARM')], default=0),
        ),
        migrations.AlterField(
            model_name='currentmortgage',
            name='current_term',
            field=models.CharField(help_text='(months remaining)', max_length=255, verbose_name='Current Term'),
        ),
        migrations.AlterField(
            model_name='currentmortgage',
            name='date_loan_originated',
            field=models.DateField(help_text='(mm/dd/yyyy)', verbose_name='Date Loan Originated'),
        ),
        migrations.AlterField(
            model_name='loanpaymenthistory',
            name='interest_pmt',
            field=models.DecimalField(decimal_places=4, max_digits=12, verbose_name='Interest Paid'),
        ),
        migrations.AlterField(
            model_name='loanpaymenthistory',
            name='pmt_date',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='Date Recieved'),
        ),
        migrations.AlterField(
            model_name='loanpaymenthistory',
            name='pmt_total',
            field=models.DecimalField(decimal_places=4, max_digits=12, verbose_name='Payment Recieved'),
        ),
        migrations.AlterField(
            model_name='loanpaymenthistory',
            name='principal_pmt',
            field=models.DecimalField(decimal_places=4, max_digits=12, verbose_name='Principal Paid'),
        ),
        migrations.AlterField(
            model_name='mortgagedesired',
            name='loan_type_desired',
            field=models.IntegerField(choices=[(0, 'Fixed'), (1, 'ARM')], default=0, verbose_name='Desired Loan Type'),
        ),
    ]
