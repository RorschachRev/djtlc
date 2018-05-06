from django.db import models
from wwwtlc.models import Address
from wwwtlc.models import Contract
from django.utils import timezone

# Create your models here.

class Loan(models.Model):
	loan_ID = models.CharField(max_length=254)
	loan_address = models.CharField(max_length=254)
	borrower_id = models.CharField(max_length=254)
	contact_person_id = models.CharField(max_length=254)
	loan_officer_id = models.CharField(max_length=254)
	loan_data_id = models.CharField(max_length=254) # * what data type should this be?
	loan_payment_monthly = models.DecimalField(decimal_places=4, max_digits=100)
	estimated_payments = models.IntegerField()
	loan_request_date = models.DateField(default=timezone.now) #creates timestamp upon entry, and allows for edits
	
	def __str__(self):
		return self.loan_ID

class Loan_Data(models.Model):
	loan = models.ForeignKey(Loan)
	loan_address = Loan.loan_address
	LOAN_STATUS_CHOICES = (
			('active','active'),
			('suspended', 'suspended'),
			('foreclosure', 'foreclosure'),
			('closed', 'closed'),
		)
	loan_status = models.CharField(max_length=12,
							choices=LOAN_STATUS_CHOICES,
							default='active'
							)
	data_id = models.CharField(max_length=30, default='NULL')
	loan_balance = models.DecimalField(decimal_places=2, max_digits=100) # (BC) *
	loan_intrate_current = models.DecimalField(decimal_places=2, max_digits=100)
	loan_intrate_start = models.DecimalField(decimal_places=2, max_digits=100)
	loan_principle = models.DecimalField(decimal_places=2, max_digits=100) # *
	loan_principle_paid = models.DecimalField(decimal_places=2, max_digits=100)
	loan_interest_paid = models.DecimalField(decimal_places=2, max_digits=100)
	LOAN_TYPE_CHOICES = (
			('TYPE_FIXED', 'TYPE_FIXED'),
			('TYPE_ARM', 'TYPE_ARM'),
		)
	loan_type = models.CharField(max_length=12,
							choices=LOAN_TYPE_CHOICES,
							default='TYPE_FIXED'
							)
	loan_currency = models.CharField(max_length=3, default='USD') #(USD) - default
	loan_partner = models.CharField(max_length=254)
	
	borrower_id = Loan.borrower_id
	contact_person_id = Loan.contact_person_id
	loan_officer_id = Loan.loan_officer_id
	loan_data_id = Loan.loan_data_id
	loan_payment_monthly = Loan.loan_payment_monthly # *
	estimated_payments = Loan.estimated_payments #integer
	addressID = Loan.loan_address #(street, city, state, zip, country)
	contracts = Contract.refkey# - from wwwtlc models.py
	loan_request_date = Loan.loan_request_date
	loan_approve_date = models.DateField()
	
	def __str__(self):
		return self.data_id
