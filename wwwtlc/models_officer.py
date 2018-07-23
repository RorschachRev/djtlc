import datetime
from decimal import Decimal

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

from wwwtlc.models_meta import Wallet, Person
from wwwtlc.models_bse import ApplicationSummary, BorrowerInfo

class LenderInfo(models.Model):
	DECISION_CHOICES = (
		(0, 'Approved'),
		(1, 'Denied'),
		(2, 'Incomplete'),
		(3, 'Counteroffer'),
		(4, 'Conditional Approval'),
		(5, 'Withdrawl'),
		(6, 'Other'),
	)
	loan_officer = models.ForeignKey(User, limit_choices_to = {'is_staff__exact': True }, related_name='loan_officer', verbose_name='Loan Officer')
	officer_number = models.IntegerField(help_text='(required)', verbose_name='Officer Number')
	approved_by = models.ForeignKey(User, limit_choices_to = {'is_staff__exact': True }, related_name='loan_approver', verbose_name='Approved By')
	concurrence_by = models.ForeignKey(User, limit_choices_to = {'is_staff__exact': True }, related_name='loan_concurrer', verbose_name='Concurrence By') # 'loan_concurrer' <- yikes
	committee_date = models.DateField(verbose_name='Committee Date', help_text='(required)')
	branch = models.CharField(max_length=256, help_text='(required)') # this could be an Address (?)
	app_date = models.DateField(verbose_name='Application Date', help_text='(required)')
	app_number = models.IntegerField(verbose_name='Application Number', help_text='(required)')
	commitment_number = models.IntegerField(verbose_name='Commitment Number', help_text='(required)')
	loan_number = models.IntegerField(verbose_name='Loan Number', help_text='(required)')
	mortgage_loan_originator_id = models.CharField(max_length=256, verbose_name='Mortgage Loan Originator ID', help_text='(required)')# may turn into FK with 'user__is_staff__exact':True
	mortgage_loan_company_id = models.CharField(max_length=256, verbose_name='Morgage Loan Origination Company ID', help_text='(required)') # will probably turn into FK - unsure to what table though, may need to make a new one
	decision = models.IntegerField(
		choices = DECISION_CHOICES,
		default = 0,
	)
	decision_date = models.DateField(verbose_name='Decision Date', help_text='(required)')
	
	def __str__(self):
		return str(self.app_number) + ' | Decision: ' + str(self.DECISION_CHOICES[self.decision]) + ', ' + str(self.decision_date)
		
class LoanTerms (models.Model):
	MORTGAGE_CHOICES = (
		(0, 'VA'),
		(1, 'FHA'),
		(2, 'Conventional'),
		(3, 'USDA/Rural Housing Service'),
		(4, 'Other'),
	)
	AMORTIZATION_CHOICES = (
		(0, 'Fixed Rate'),
		(1, 'GPM'),
		(2, 'ARM (type)'),
		(3, 'Other'),
	)
	mortgage_applied = models.IntegerField(
		choices = MORTGAGE_CHOICES,
		default = 0,
		verbose_name = 'Mortgage Type'
	)
	agency_case_no = models.IntegerField(verbose_name='Agency Case Number', help_text='(required)')
	lender_case_no = models.IntegerField(verbose_name='Lender Case Number', help_text='(required)')
	application = models.ForeignKey(ApplicationSummary, null=True, blank=True)
	loan_amount = models.DecimalField(max_digits=12, decimal_places=4, verbose_name='Loan Amount', help_text='(required)')
	int_rate = models.DecimalField(max_digits=4, decimal_places=2, verbose_name='Interest Rate', help_text='(required)')
	months_left = models.IntegerField(verbose_name='Months Left on Loan', help_text='(required)')
	amortization_type = models.IntegerField(
		choices = AMORTIZATION_CHOICES,
		default = 0,
		verbose_name = 'Amortization Type',
	)
	
	def __str__(self):
		return 'Lender Case Number: ' + str(self.lender_case_no) + ', Loan Amount: ' + str(self.loan_amount)
		
class NewLoan(models.Model):
	user = models.ForeignKey(User)
	borrower = models.ForeignKey(BorrowerInfo, related_name='loan_borrower')
	coborrower = models.ForeignKey(BorrowerInfo, related_name='loan_coborrower', null=True, blank=True)
	loan_terms = models.ForeignKey(LoanTerms) # contains all originally agreed upon numbers
	payment_due = models.DecimalField(decimal_places=4, max_digits=12)
	payment_due_date = models.IntegerField()
	payments_left = models.IntegerField()
	principal_balance = models.DecimalField(decimal_places=18, max_digits=65)
	loan_intrate_current = models.DecimalField(decimal_places=2, max_digits=4)
	principal_paid = models.DecimalField(decimal_places=4, max_digits=12)
	interest_paid = models.DecimalField(decimal_places=4, max_digits=12)
	loan_wallet = models.OneToOneField(Wallet)
	TLC_balance = models.DecimalField(decimal_places=18, max_digits=65)
	
	def __str__(self):
		return str(self.user) + ', ' + str(self.loan_wallet)
		
class LoanSummary(models.Model):
	application = models.ForeignKey(ApplicationSummary, verbose_name='Application Summary')
	lender_info = models.ForeignKey(LenderInfo, verbose_name='Lender Information')
	loan_terms = models.ForeignKey(LoanTerms, verbose_name='Loan Terms')
	
	def __str__(self):
		return str(self.loan_terms)
		
class LoanPaymentHistory(models.Model):
	wallet = models.ForeignKey(Wallet)
	loan = models.ForeignKey(NewLoan)
	pmt_total = models.DecimalField(decimal_places=4, max_digits=12)
	principal_pmt = models.DecimalField(decimal_places=4, max_digits=12)
	interest_pmt = models.DecimalField(decimal_places=4, max_digits=12)
	pmt_date = models.DateTimeField(default=timezone.now)