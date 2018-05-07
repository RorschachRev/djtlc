from django.db import models
from wwwtlc.models import Address, Contract, People
from django.utils import timezone

# Create your models here.

class Loan(models.Model):
	loan_id = models.AutoField(primary_key=True)
	borrower_id = models.Integer()
	contact_person_id = models.ForeignKey(People, related_name='contact_person')
	loan_officer_id = models.ForeignKey(People, related_name='loan_officer')
	loan_data_id = models.Integer()
	loan_address = models.CharField(max_length=254)
	loan_payment_monthly = models.DecimalField(decimal_places=5, max_digits=20)
	estimated_payments = models.IntegerField()
	loan_request_date = models.DateField(default=timezone.now) #creates timestamp upon entry, and allows for edits
	
	def __str__(self):
		return self.loan_ID

class Loan_Data(models.Model):
	data_id = models.Integer()
	loan = models.ForeignKey(Loan)
	loan_address = models.ForeignKey(Address)
	contracts = models.ForeignKey(Contract)
	borrower_id = models.ForeignKey(Loan, related_name='borrower')
	loan_data_id = models.ForeignKey(Loan, related_name='loan_data')
	contact_person_id = models.ForeignKey(Loan, related_name='contact_person')
	loan_officer_id = models.ForeignKey(Loan, related_name='loan_officer')
	LOAN_STATUS_CHOICES = (
			(0, 'active'),
			(1, 'suspended'),
			(2, 'foreclosure'),
			(3, 'closed'),
		)
	loan_status = models.CharField(max_length=10,
							choices=LOAN_STATUS_CHOICES,
							default=0
							)
	loan_balance = models.DecimalField(decimal_places=5, max_digits=10) # (BC) *
	loan_intrate_current = models.DecimalField(decimal_places=2, max_digits=4)
	loan_intrate_start = models.DecimalField(decimal_places=2, max_digits=4)
	loan_principle = models.DecimalField(decimal_places=2, max_digits=10) # *
	loan_principle_paid = models.DecimalField(decimal_places=5, max_digits=10)
	loan_interest_paid = models.DecimalField(decimal_places=5, max_digits=10)
	LOAN_TYPE_CHOICES = (
			(0, 'TYPE_FIXED'),
			(1, 'TYPE_ARM'),
		)
	loan_type = models.CharField(max_length=10,
							choices=LOAN_TYPE_CHOICES,
							default=0
							)
	loan_currency = models.CharField(max_length=3, default='USD') #(USD) - default
	loan_partner = models.CharField(max_length=254)
	loan_approve_date = models.DateField()
	TLC_balance = models.DecimalField(decimal_places=5, max_digits=10) # (BC) * ADMIN ONLY
	
	def __str__(self):
		return self.data_id