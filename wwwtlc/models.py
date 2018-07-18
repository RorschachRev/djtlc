import datetime
from decimal import Decimal
from django.db import models
from django.contrib.auth.models import User



from django.utils import timezone

#Extend User to include Wallet FK_ID


#NoSQL Section
class Contract(models.Model):
	refkey=models.IntegerField()
	def __str__(self):
		return str(self.refkey)
class Credit_Report(models.Model):
	refkey=models.IntegerField()
	def __str__(self):
		return str(self.refkey)
class Bank(models.Model):
	refkey=models.IntegerField()
	def __str__(self):
		return str(self.refkey)
class Bank_Account(models.Model):
	refkey=models.IntegerField()
	def __str__(self):
		return str(self.refkey)
class Borrower(models.Model):
	refkey=models.IntegerField()
	def __str__(self):
		return str(self.refkey)
class Partner(models.Model):
	refkey=models.IntegerField()
	def __str__(self):
		return str(self.refkey)


#Structured Data
class Address(models.Model):
	street1=models.CharField(max_length=254, help_text="The street address of the property needing financed", verbose_name="Street 1")
	street2=models.CharField(max_length=254, blank=True, verbose_name="Street 2", help_text="(optional)")
	street3=models.CharField(max_length=254, blank=True, verbose_name="Street 3", help_text="(optional)")
	city=models.CharField(max_length=127)
	state=models.CharField(max_length=25)
	zipcode=models.CharField(max_length=10)
	country	=models.CharField(max_length=3)
	
	def __str__(self):
		return self.street1

class Verified(models.Model):
	ver_none = 0
	ver_ID = 1
	ver_KYC = 2
	ver_QInv = 3
	VERIFIED_CHOICES = (
			(ver_none, 'Not Verified'),
			(ver_ID, 'ID Verified'),
			(ver_KYC, 'KYC Verified'),
			(ver_QInv, 'Qualified Investor'),
		)
	verified_level = models.IntegerField(
			choices=VERIFIED_CHOICES,
			default=ver_none,
		)
	ver_none_apply_date= models.DateTimeField(default=timezone.now, blank=True, null=True, verbose_name="Not verified application date")
	ver_none_approved_date =models.DateTimeField(blank=True, null=True,verbose_name="Not verified approval date")
	ver_ID_apply_date=models.DateTimeField(blank=True, null=True, verbose_name="ID verification application date")
	ver_ID_approved_date=models.DateTimeField(blank=True, null=True, verbose_name="ID verification approval date")
	ver_KYC_apply_date=models.DateTimeField(blank=True, null=True, verbose_name="KYC verification application date")
	ver_KYC_approved_date=models.DateTimeField(blank=True, null=True, verbose_name="KYC verification approval date")
	ver_QInv_apply_date=models.DateTimeField(blank=True, null=True, verbose_name="Qualified investor application date")
	ver_QInv_approved_date=models.DateTimeField(blank=True, null=True, verbose_name="Qualified investor approval date")

	def __str__(self):
		z = self.ver_none_apply_date
		
		return str(self.VERIFIED_CHOICES[self.verified_level]) + ' ' + str(z)

class Person(models.Model):
	#user = models.ForeignKey('auth.User')
	#user = models.OneToOneField(User, primary_key=True, blank=True, null=True)
	user = models.OneToOneField(User, blank=True, null=True)
	name_first = models.CharField(max_length=30, verbose_name="First Name")
	name_middle= models.CharField(max_length=30, blank=True, verbose_name="Middle Name", help_text="(optional)")
	name_last= models.CharField(max_length=30, verbose_name="Last Name")
	phone= models.CharField(max_length=15, help_text="Please use this format: (xxx) xxx-xxxx")
	email_address = models.CharField(max_length=100, blank=True, null=True, verbose_name="Email Address")
	taxid= models.CharField(max_length=12, blank=True, null=True, verbose_name="Tax ID")
	language= models.CharField(max_length=3)

	verified=models.ForeignKey(Verified, blank=True, null=True)
	address=models.ForeignKey(Address, blank=True, null=True, help_text="The address of the property needing financed")
	credit=models.ForeignKey(Credit_Report, blank=True, null=True)
	bank_info=models.ManyToManyField(Bank, blank=True, verbose_name="Bank Information")
	bank_acct=models.ManyToManyField(Bank_Account, blank=True, verbose_name="Bank Account")

	def __str__(self):
		return self.name_first + ' ' + self.name_last
		
class Wallet(models.Model):
	wallet = models.ForeignKey(User)
	address=models.CharField(max_length=127)
	blockchain=models.CharField(max_length=4)
	buy_TLC_approval=models.NullBooleanField()
	#date_added
	TLC_balance_USD=models.DecimalField(decimal_places=2, max_digits=12, null=True, blank=True)
	TLC_balance_Token=models.DecimalField(decimal_places=18, max_digits=64, null=True, blank=True)	# (BC is 79, total supply is 27 with 18 decimal)
		#max mysql is 65 digits
	def __str__(self):
		return self.address[:8]+"..."
		

#Payments
#Business
#Fees


'''
Super disgusting hack and slash models to meet requirements of new loanapply form
specified in email recieved on 7/17.
'''
class ContactRequest(models.Model):
	first_name = models.CharField(max_length=255)
	last_name = models.CharField(max_length=255)
	phone = models.CharField(max_length=255)
	email_address = models.CharField(max_length=255)
	
class PropertyInfoRequest(models.Model):
	property_type = models.CharField(max_length=255)
	property_use = models.CharField(max_length=255)
	occupancy_rate = models.DecimalField(decimal_places=4, max_digits=12)
	lease_rate = models.DecimalField(decimal_places=4, max_digits=12)
	rent = models.DecimalField(decimal_places=4, max_digits=12)
	property_address = models.CharField(max_length=255)
	property_age = models.IntegerField()
	
class CurrentMortgage(models.Model):
	date_loan_originated = models.DateField()
	current_loan_type = models.CharField(max_length=255)
	original_amount = models.DecimalField(decimal_places=4, max_digits=12)
	current_balance = models.DecimalField(decimal_places=4, max_digits=12)
	current_term = models.CharField(max_length=255)
	current_intrate = models.DecimalField(decimal_places=2, max_digits=4)
	late_payments = models.BooleanField(default=False)
	
class MortgageDesired(models.Model):
	amount_desired = models.DecimalField(decimal_places=4, max_digits=12)
	cash_back_desired = models.DecimalField(decimal_places=4, max_digits=12)
	loan_currency = models.CharField(max_length=3, default='USD')
	loan_type_desired = models.CharField(max_length=255)
	payment_desired = models.DecimalField(decimal_places=4, max_digits=12)
	intrate_desired = models.DecimalField(decimal_places=2, max_digits=4)
	time_frame = models.CharField(max_length=255)
	term_desired = models.CharField(max_length=255)
	
class BorrowerInfoRequest(models.Model):
	B_TYPE_CHOICES = (
		(0, 'Personal'),
		(1, 'Business'),
	)
	language = models.CharField(max_length=3)
	type = models.IntegerField(
		default = 0,
		choices = B_TYPE_CHOICES,
	)
	annual_income = models.DecimalField(decimal_places=4, max_digits=12)
	net_worth = models.DecimalField(decimal_places=4, max_digits=12)
	fico = models.CharField(max_length=255)
	
class NewRequestSummary(models.Model):
	STATUS_CHOICES = (
		(0, 'Sleep'),
		(1, 'Active'),
		(2, 'Priority'),
		(3, 'Tier 1'),
		(4, 'Tier 2'),
	)
	status = models.IntegerField(
		default = 1,
		choices = STATUS_CHOICES,
	)
	user = models.ForeignKey(User)
	contact = models.ForeignKey(ContactRequest)
	property = models.ForeignKey(PropertyInfoRequest)
	curr_mortgage = models.ForeignKey(CurrentMortgage)
	desired_mortgage = models.ForeignKey(MortgageDesired)
	borrower = models.ForeignKey(BorrowerInfoRequest)
	submitted = models.DateTimeField(default=timezone.now)