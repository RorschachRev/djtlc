from django.db import models
from wwwtlc.models import Address, Contract, Person, Borrower, Partner, Verified
from django.utils import timezone

# Create your models here.

class Loan_Data(models.Model):
	loan_address = models.ForeignKey(Address)
	contracts = models.ForeignKey(Contract)
	contact_person = models.ForeignKey(Person, related_name='contact_person')
	LOAN_STATUS_CHOICES = (
			(0, 'active'),
			(1, 'suspended'),
			(2, 'foreclosure'),
			(3, 'closed'),
		)
	loan_status = models.IntegerField(
			choices=LOAN_STATUS_CHOICES,
			default=0
		)
	borrower_requested = models.CharField(max_length=60) #At time of loan request, who is trying to borrow the money
	BORROWER_TYPE_CHOICES = (
			(0, 'Individual'),
			(1, 'Married Couple'),
			(2, 'Partnership'),
			(3, 'Corporation'),
			(4, 'Limited Liability Company'),
			(5, 'Trust'),
			(6, 'Investment Group'),
			(7, 'Other'),
		)
	borrower_type = models.IntegerField(
			choices=BORROWER_TYPE_CHOICES,
			default=0
		)
	loan_balance = models.DecimalField(decimal_places=18, max_digits=80) # (BC is 79)
	loan_intrate_current = models.DecimalField(decimal_places=2, max_digits=4)
	loan_intrate_start = models.DecimalField(decimal_places=2, max_digits=4)
	loan_principle = models.DecimalField(decimal_places=2, max_digits=12) 
	loan_principle_paid = models.DecimalField(decimal_places=4, max_digits=15)
	loan_interest_paid = models.DecimalField(decimal_places=4, max_digits=15)
	LOAN_TYPE_CHOICES = (
			(0, 'TYPE_FIXED'),
			(1, 'TYPE_ARM'),
			#(2, 'TYPE_SHARIAH'),
		)
	loan_type = models.IntegerField(
			choices=LOAN_TYPE_CHOICES,
			default=0
		)
	loan_currency = models.CharField(max_length=3, default='USD') #(USD) - default
	loan_partner = models.ForeignKey(Partner, related_name='loan_partner')	#NoSQL
	loan_approve_date = models.DateField()
	TLC_balance = models.DecimalField(decimal_places=18, max_digits=80) # (BC is 79, total supply is 27 with 18 decimal) * ADMIN ONLY
	
	def __str__(self):
		return self.data_id

class Loan(models.Model):
	borrower_id = models.ForeignKey(Borrower, related_name='borrower')	#NoSQL
	loan_officer = models.ForeignKey(Person, related_name='loan_officer')
	loan_data = models.ForeignKey(Loan_Data, related_name='loan_data')
	loan_address = models.ForeignKey(Address, related_name='loan_address')
	loan_payment_request = models.DecimalField(decimal_places=4, max_digits=12)
	loan_payment_required = models.DecimalField(decimal_places=4, max_digits=12)
	loan_payment_quantity = models.IntegerField()
	loan_request_date = models.DateField(default=timezone.now) #creates timestamp upon entry, and allows for edits
	
	def __str__(self):
		return self.loan_ID