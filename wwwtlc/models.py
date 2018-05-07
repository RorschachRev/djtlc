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
class Address(models.Model):
	street1=models.CharField(max_length=254)
	street2=models.CharField(max_length=254)
	street3=models.CharField(max_length=254)
	city=models.CharField(max_length=127)
	state=models.CharField(max_length=25)
	zipcode=models.CharField(max_length=10)
	country	=models.CharField(max_length=3)

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
    ver_none_apply_date= models.DateTimeField(default=timezone.now)
    ver_none_approved_date =models.DateTimeField()
    ver_ID_apply_date=models.DateTimeField()
    ver_ID_approved_date=models.DateTimeField()
    ver_KYC_apply_date=models.DateTimeField()
    ver_KYC_approved_date=models.DateTimeField()
    ver_QInv_apply_date=models.DateTimeField()
    ver_QInv_approved_date=models.DateTimeField()

class Person(models.Model):
	user = models.ForeignKey('auth.User')
	name_first = models.CharField(max_length=30)
	name_middle= models.CharField(max_length=30)
	name_last= models.CharField(max_length=30)
	phone= models.CharField(max_length=15)
	taxid= models.CharField(max_length=12)
	language= models.CharField(max_length=3)

	verified=models.ForeignKey(Verified)
	address=models.ForeignKey(Address)
	credit=models.ForeignKey(Credit_Report)
	bank_info=models.ManyToManyField(Bank)
	bank_acct=models.ManyToManyField(Bank_Account)

	def __str__(self):
		return self.title

#Payments
#Business
#Fees
