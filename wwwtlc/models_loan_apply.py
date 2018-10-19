import datetime
from decimal import Decimal
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.validators import MinValueValidator

# For the most part, this models file is straightforward,
# the only things that I would like to know about it would be
# what values I should use for things like 'max_length' and
# 'max_digits', as well as which value should be default on
# the CHOICES fields

class Address(models.Model):
	user = models.ForeignKey(User)
	source = models.ForeignKey(User, related_name='address_source')
	street1 = models.CharField(max_length=254, help_text="The street address of the property needing financed", verbose_name="Street 1")
	street2 = models.CharField(max_length=254, blank=True, verbose_name="Street 2", help_text="(optional)")
	street3 = models.CharField(max_length=254, blank=True, verbose_name="Street 3", help_text="(optional)")
	city = models.CharField(max_length=127)
	state = models.CharField(max_length=25)
	zipcode = models.CharField(max_length=10, blank=True, null=True)
	country = models.CharField(max_length=3, default = 'US')
	
	def __str__(self):
		return self.street1 + ', ' + self.city + ', ' + self.state 

class ContactRequest(models.Model):
	source = models.ForeignKey(User)
	name_first = models.CharField(max_length=255, verbose_name='First Name')
	name_middle = models.CharField(max_length=30, blank=True, null=True, verbose_name='Middle Name', help_text='(optional)')
	name_last = models.CharField(max_length=255, verbose_name='Last Name')
	phone = models.CharField(max_length=255, verbose_name='Phone Number')
	email_address = models.CharField(max_length=255, verbose_name='Email')
	
class PropertyInfoRequest(models.Model):
	TYPE_CHOICES = (
		(0, 'Commercial'),
		(1, 'Industrial'),
		(2, 'Residential'),
		(3, 'Mixed'),
		(4, 'Select Property Type'),
	)
	property_type = models.IntegerField(
		choices = TYPE_CHOICES,
		default = 4,
		verbose_name='Property Type'
	)
	source = models.ForeignKey(User)
	property_address = models.ForeignKey(Address, help_text="Select property from list, or click '+' to add new property.")
	occupancy_rate = models.DecimalField(decimal_places=4, max_digits=12, blank=True, null=True, validators=[MinValueValidator(0)], verbose_name='Occupancy Rate')
	lease_rate = models.DecimalField(decimal_places=4, max_digits=12, blank=True, null=True, validators=[MinValueValidator(0)], verbose_name='Lease Rate')
	rent = models.DecimalField(decimal_places=4, max_digits=12, validators=[MinValueValidator(0)], verbose_name='Current Loan Payment')
	property_age = models.IntegerField(validators=[MinValueValidator(0)], verbose_name='Property Age')
	
class CurrentMortgage(models.Model):
	TYPE_CHOICES = (
		(0, 'Fixed'),
		(1, 'ARM'),
	)
	LATE_CHOICES = (
		(0, 'No'),
		(1, 'Yes'),
		(2, 'Select'),
	)
	source = models.ForeignKey(User)
	date_loan_originated = models.CharField(max_length=30, verbose_name='Date Loan Originated')
	current_loan_type = models.IntegerField(
		choices = TYPE_CHOICES,
		default = 0,
	)
	original_amount = models.DecimalField(decimal_places=4, max_digits=12, validators=[MinValueValidator(0)], verbose_name='Original Amount')
	current_balance = models.DecimalField(decimal_places=4, max_digits=12, validators=[MinValueValidator(0)], verbose_name='Current Balance')
	current_term = models.CharField(max_length=255, verbose_name='Current Term', help_text='Months remaining of total (e.g. 45 of 120)')
	current_intrate = models.DecimalField(decimal_places=2, max_digits=4, validators=[MinValueValidator(0)], verbose_name='Current Interest Rate')
	late_payments = models.IntegerField(
		choices = LATE_CHOICES,
		default = 2,
		verbose_name = "Have you made any late payments?",
	)
	
class MortgageDesired(models.Model):
	TYPE_CHOICES = (
		(0, 'Fixed'),
		(1, 'ARM'),
	)
	TIMEFRAME_CHOICES = (
		(0, 'Immediately'),
		(1, 'Within a Month'),
		(2, 'Within 6 Months'),
	)
	TERM_CHOICES = (
		(0, '20 Year'),
		(1, '15 Year'),
		(2, '10 Year'),
		(3, 'Less than 10 Years'),
		(4, 'Not Listed / Not Sure'),
	)
	source = models.ForeignKey(User)
	amount_desired = models.DecimalField(decimal_places=4, max_digits=12, validators=[MinValueValidator(0)], verbose_name='Amount Desired')
	cash_back_desired = models.DecimalField(decimal_places=4, max_digits=12, validators=[MinValueValidator(0)], verbose_name='Cash Back Desired')
	loan_currency = models.CharField(max_length=3, default='USD', verbose_name='Loan Currency')
	loan_type_desired = models.IntegerField(
		choices = TYPE_CHOICES,
		default = 0,
		verbose_name='Desired Loan Type'
	)
	payment_desired = models.DecimalField(decimal_places=4, max_digits=12, validators=[MinValueValidator(0)], verbose_name='Desired Payment of About')
	intrate_desired = models.DecimalField(decimal_places=2, max_digits=4, validators=[MinValueValidator(0)], verbose_name='Desired Interest Rate')
	time_frame = models.IntegerField(
		choices = TIMEFRAME_CHOICES,
		default = 0,
		verbose_name='Ready to Move Forward'
	)
	term_desired = models.IntegerField(
		choices = TERM_CHOICES,
		default = 0,
		verbose_name='Desired Term'
	)
	
class BorrowerInfoRequest(models.Model):
	B_TYPE_CHOICES = (
		(0, 'Business'),
		(1, 'Personal'),
	)
	FICO_CHOICES = (
		(0, '720+'),
		(1, '690-719'),
		(2, '660-679'),
		(3, '630-659'),
		(4, 'Unknown'),
		(5, 'Select'),
	)
	source = models.ForeignKey(User)
	language = models.CharField(default='en-us', max_length=8, null=True, blank=True)# hidden field, for now
	type = models.IntegerField(
		default = 0,
		choices = B_TYPE_CHOICES,
		verbose_name='Type'
	)
	annual_income = models.DecimalField(decimal_places=4, max_digits=12, validators=[MinValueValidator(0)], verbose_name='Annual Income')
	net_worth = models.DecimalField(decimal_places=4, max_digits=12, validators=[MinValueValidator(0)], verbose_name='Net Worth')
	fico = models.IntegerField(
		choices = FICO_CHOICES,
		default = 5,
		verbose_name='FICO',
		help_text='(approximate credit score)'
	)
	
class NewRequestSummary(models.Model):
	STATUS_CHOICES = (
		(0, 'Sleep'),
		(1, 'Active'),
		(2, 'Priority'),
		(3, 'Basic'),
		(4, 'Standard'),
		(5, 'Submitted'),
		#(5, 'Extended'), # would swap places with 'submitted', waiting on information
	)
	status = models.IntegerField(
		default = 1,
		choices = STATUS_CHOICES,
	)
	user = models.ForeignKey(User)
	source = models.ForeignKey(User, related_name='new_request_summary_source')
	contact = models.ForeignKey(ContactRequest)
	property = models.ForeignKey(PropertyInfoRequest)
	curr_mortgage = models.ForeignKey(CurrentMortgage, verbose_name='Current Mortgage')
	desired_mortgage = models.ForeignKey(MortgageDesired, verbose_name='Desired Mortgage')
	borrower = models.ForeignKey(BorrowerInfoRequest)
	submitted = models.DateTimeField(default=timezone.now)
