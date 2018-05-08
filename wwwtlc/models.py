import datetime
from decimal import Decimal
from django.db import models


from django.utils import timezone

#Extend User to include Wallet FK_ID


#NoSQL Section
class Contract(models.Model):
	refkey=models.IntegerField()
	def __str__(self):
		return self.title
class Credit_Report(models.Model):
	refkey=models.IntegerField()
	def __str__(self):
		return self.title
class Bank(models.Model):
	refkey=models.IntegerField()
	def __str__(self):
		return self.title
class Bank_Account(models.Model):
	refkey=models.IntegerField()
	def __str__(self):
		return self.title
class Borrower(models.Model):
	refkey=models.IntegerField()
	def __str__(self):
		return self.title
class Partner(models.Model):
	refkey=models.IntegerField()
	def __str__(self):
		return self.title


#Structured Data
class Wallet(models.Model):
	address=models.CharField(max_length=127)
	blockchain=models.CharField(max_length=4)
	TLC_balance = models.DecimalField(decimal_places=18, max_digits=80) # (BC is 79, total supply is 27 with 18 decimal)
	
	def __str__(self):
		return self.address

class Address(models.Model):
	street1=models.CharField(max_length=254)
	street2=models.CharField(max_length=254, blank=True)
	street3=models.CharField(max_length=254, blank=True)
	city=models.CharField(max_length=127)
	state=models.CharField(max_length=25)
	zipcode=models.CharField(max_length=10)
	country	=models.CharField(max_length=3)
	
	#this allows django/admin foreign key in Loan_Data to drop down a list of addresses
	def __str__(self):
		return self.street1

class Verified(models.Model): # whole model can't accept null fields: IntegrityError NOTNULL constraint failed
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
	ver_none_apply_date= models.DateTimeField(default=timezone.now)
	ver_none_approved_date =models.DateTimeField()
	ver_ID_apply_date=models.DateTimeField()
	ver_ID_approved_date=models.DateTimeField()
	ver_KYC_apply_date=models.DateTimeField()
	ver_KYC_approved_date=models.DateTimeField()
	ver_QInv_apply_date=models.DateTimeField()
	ver_QInv_approved_date=models.DateTimeField()

	#will probably want to change this later
	def __str__(self):
		x = self.verified_level
		y = ''
		
		if x == 0:
			y='Not Verified'
		elif x == 1:
			y='ID Verified'
		elif x == 2:
			y='KYC Verified'
		elif x == 3:
			y='Qualified Investor'
		
		return y

class Person(models.Model):
	user = models.ForeignKey('auth.User')
	name_first = models.CharField(max_length=30)
	name_middle= models.CharField(max_length=30, blank=True)
	name_last= models.CharField(max_length=30)
	phone= models.CharField(max_length=15, help_text="Please use this format: (xxx) xxx-xxxx")
	taxid= models.CharField(max_length=12)
	language= models.CharField(max_length=3)

	verified=models.ForeignKey(Verified)
	address=models.ForeignKey(Address)
	credit=models.ForeignKey(Credit_Report) # can't accept null fields: IntegrityError NOTNULL constraint failed
	bank_info=models.ManyToManyField(Bank) # can't accept null fields: IntegrityError NOTNULL constraint failed
	bank_acct=models.ManyToManyField(Bank_Account) # can't accept null fields: IntegrityError NOTNULL constraint failed


#Payments
#Business
#Fees
