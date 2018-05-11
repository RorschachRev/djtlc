from django.db import models
from wwwtlc.models import Address, Contract, Person, Borrower, Partner, Verified, Wallet
from django.utils import timezone

# Create your models here.

class Loan_Data(models.Model):
	loan_address = models.ForeignKey(Address, help_text="The address of the property needing financed")
	contracts = models.ForeignKey(Contract, blank=True, null=True, help_text="(optional)")
	contact_person = models.ForeignKey(Person, related_name='contact_person', help_text="The facilitator for loan processing")
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
	borrower_requested = models.CharField(max_length=60, verbose_name="Borrower", help_text="At time of loan request, the person/entity trying to borrow the money") #At time of loan request, who is trying to borrow the money
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
	loan_balance = models.DecimalField(decimal_places=18, max_digits=80, null=True, blank=True, help_text="Remaining balance left on loan") # (BC is 79)
	loan_intrate_current = models.DecimalField(decimal_places=2, max_digits=4, null=True, blank=True, verbose_name="Current interest rate")
	loan_intrate_start = models.DecimalField(decimal_places=2, max_digits=4, null=True, blank=True, verbose_name="Starting interest rate")
	loan_principle = models.DecimalField(decimal_places=2, max_digits=12, null=True, blank=True) 
	loan_principle_paid = models.DecimalField(decimal_places=4, max_digits=15, null=True, blank=True)
	loan_interest_paid = models.DecimalField(decimal_places=4, max_digits=15, null=True, blank=True)
	LOAN_TYPE_CHOICES = (
			(0, 'FIXED'),
			(1, 'ARM'),
			#(2, 'TYPE_SHARIAH'),
		)
	loan_type = models.IntegerField(
			choices=LOAN_TYPE_CHOICES,
			default=0
		)
	loan_currency = models.CharField(max_length=3, default='USD') #(USD) - default
	loan_partner = models.ForeignKey(Partner, related_name='loan_partner', blank=True, null=True, help_text = '(optional)')	#NoSQL
	loan_approve_date = models.DateField(blank=True, null=True)
	TLC_balance = models.ForeignKey(Wallet, related_name='balances', null=True, blank=True)
	
	def __str__(self):
		return str(self.contact_person) + ', ' + str(self.loan_address) #this will display the name of the contact person, and the address of the property needing financing

class Loan(models.Model):
	borrower_id = models.ForeignKey(Borrower, related_name='borrower', verbose_name="Borrower ID")	#NoSQL
	loan_officer = models.ForeignKey(Person, related_name='loan_officer')
	loan_data = models.ForeignKey(Loan_Data, related_name='loan_data')
	loan_address = models.ForeignKey(Address, related_name='loan_address', help_text="The address of the property needing financed")
	loan_payment_request = models.DecimalField(decimal_places=4, max_digits=12, help_text="Desired monthly payment")
	loan_payment_required = models.DecimalField(decimal_places=4, max_digits=12, help_text="Approved monthly payment")
	loan_payment_quantity = models.IntegerField(help_text="Months until loan is paid")
	loan_request_date = models.DateField(default=timezone.now) #creates timestamp upon entry, and allows for edits
	
	def __str__(self):
		return self.loan_ID