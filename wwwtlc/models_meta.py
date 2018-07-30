import datetime
from decimal import Decimal
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

from wwwtlc.models_bse import BorrowerInfo, ApplicationSummary
from wwwtlc.models_loan_apply import Address

#Extend User to include Wallet FK_ID


#NoSQL Section
class Contract(models.Model):
	source = models.ForeignKey(User, null=True, blank=True)
	refkey=models.IntegerField()
	def __str__(self):
		return str(self.refkey)
class Credit_Report(models.Model):
	source = models.ForeignKey(User, null=True, blank=True)
	refkey=models.IntegerField()
	def __str__(self):
		return str(self.refkey)
class Bank(models.Model):
	source = models.ForeignKey(User, null=True, blank=True)
	refkey=models.IntegerField()
	def __str__(self):
		return str(self.refkey)
class Bank_Account(models.Model):
	source = models.ForeignKey(User, null=True, blank=True)
	refkey=models.IntegerField()
	def __str__(self):
		return str(self.refkey)
class Borrower(models.Model):
	source = models.ForeignKey(User, null=True, blank=True)
	refkey=models.IntegerField()
	def __str__(self):
		return str(self.refkey)
class Partner(models.Model):
	source = models.ForeignKey(User, null=True, blank=True)
	refkey=models.IntegerField()
	def __str__(self):
		return str(self.refkey)

class Documents(models.Model):
	application = models.ForeignKey(ApplicationSummary)
	credit_report = models.ForeignKey(Credit_Report)
	bank = models.ForeignKey(Bank)
	bank_account = models.ForeignKey(Bank_Account)
	borrower = models.ForeignKey(Borrower)
	partner = models.ForeignKey(Partner)


#Structured Data
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
		

# Will need to contain all FK's for every BorrowerInfo
class Person(models.Model):
	user = models.OneToOneField(User, blank=True, null=True)
	name_first = models.CharField(max_length=30, verbose_name="First Name")
	name_middle = models.CharField(max_length=30, blank=True, verbose_name="Middle Name", help_text="(optional)")
	name_last = models.CharField(max_length=30, verbose_name="Last Name")
	phone = models.CharField(max_length=15, help_text="Please use this format: (xxx) xxx-xxxx")
	email_address = models.CharField(max_length=100, blank=True, null=True, verbose_name="Email Address")
	taxid = models.CharField(max_length=12, blank=True, null=True, verbose_name="Tax ID")
	language = models.CharField(max_length=3)
	verified = models.ForeignKey(Verified, blank=True, null=True)
	address = models.ForeignKey(Address, blank=True, null=True, help_text="The address of the property needing financed")
	credit = models.ForeignKey(Credit_Report, blank=True, null=True)
	bank_info = models.ManyToManyField(Bank, blank=True, verbose_name="Bank Information")
	bank_acct = models.ManyToManyField(Bank_Account, blank=True, verbose_name="Bank Account")
	borrower_info = models.OneToOneField(BorrowerInfo)

	def __str__(self):
		return self.name_first + ' ' + self.name_last
		
class Wallet(models.Model):
	wallet = models.ForeignKey(User)
	address=models.CharField(max_length=127, verbose_name='Blockchain Address')
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