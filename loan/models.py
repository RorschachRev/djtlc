from django.db import models
from wwwtlc.models import Address, Contract, Person, Borrower, Partner, Verified, Wallet
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.

class Loan_Request(models.Model):
	borrower_requested = models.CharField(max_length=60, verbose_name="Borrower", help_text="At time of loan request, the person/entity trying to borrow the money")
	loan_request_amt = models.DecimalField(decimal_places=4, max_digits=12, verbose_name="Desired loan amount")
	loan_payment_request = models.DecimalField(decimal_places=4, max_digits=12, help_text="Desired monthly payment")
	loan_intrate_request = models.DecimalField(decimal_places=2, max_digits=4, verbose_name="Desired interest rate")
	loan_request_date = models.DateField(default=timezone.now) #creates timestamp upon entry, and allows for edits
	
	def __str__(self):
		return self.borrower_requested + ', ' + str(self.loan_request_date)
	

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
	loan_partner = models.ForeignKey(Partner, related_name='loan_partner', blank=True, null=True, default=0, help_text = '(optional)') #NoSQL
	
	def __str__(self):
		return str(self.contact_person) + ', ' + str(self.loan_address)

class Loan(models.Model):
	user = models.ForeignKey(User)
	borrower_id = models.ForeignKey(Borrower, related_name='borrower', blank=True, null=True, verbose_name="Borrower ID")	#NoSQL
	loan_data = models.OneToOneField(Loan_Data, related_name='loan_data')
	loan_payment_due = models.DecimalField(decimal_places=4, max_digits=12, help_text="Approved monthly payment")
	loan_payment_due_date = models.DateField(default=timezone.now) #datetime
	payments_left = models.IntegerField(help_text="Months until loan is paid") #loan payments remaining
	loan_balance = models.DecimalField(decimal_places=18, max_digits=80, help_text="Remaining balance left on loan") # (BC is 79)
	loan_intrate_current = models.DecimalField(decimal_places=2, max_digits=4, verbose_name="Current interest rate")
	loan_intrate_start = models.DecimalField(decimal_places=2, max_digits=4, verbose_name="Starting interest rate")
	loan_principal = models.DecimalField(decimal_places=4, max_digits=15)
	loan_principal_paid = models.DecimalField(decimal_places=4, max_digits=15)
	loan_interest_paid = models.DecimalField(decimal_places=4, max_digits=15)
	loan_approve_date = models.DateField(default=timezone.now)
	loan_wallet = models.OneToOneField(Wallet)
	TLC_balance =models.DecimalField(decimal_places=18, max_digits=80, help_text="TLC owned by TLC from loan payment") # (BC is 79)
	
	def __str__(self):
		return str(self.loan_data) + ' (' + str(self.loan_approve_date) + ')'
		
#might want to change location of this model for relation purposes
'''class Loan_Workflow(models.Model):
	loan_data = models.OneToOneField(Loan_Data)
	loan_officer = models.ForeignKey(Person, limit_choices_to = {'user__is_staff__exact': True }, related_name='loan_officer')
	COMPLETED_CHOICES = (
			(0, 'Incomplete'),
			(1, 'Processing'),
			(2, 'Completed'),
			(3, 'N/A'),
		)
	APPROVAL_CHOICES = (
			(0, 'Denied'),
			(1, 'Approved'),
		)
	request_status = models.IntegerField(
			choices=COMPLETED_CHOICES,
			default=0
		)
	approval_status = models.IntegerField(
			choices=APPROVAL_CHOICES,
			default=0
		)
	
	def __str__(self):
		return 'Officer: ' + str(self.loan_officer) + ' | Loan: ' + str(self.loan_data)'''
			
	