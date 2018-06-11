import datetime
from decimal import Decimal
from django.db import models
from django.utils import timezone

# (SUPER)Rough Draft of models from Commercial_loan_app_transcript.txt
# Will need extensive modifying - possibly within the djtlc/loan/models.py file as well
# To be used in addition with models.loan_app2.py (seperated for pdf referencing purposes)

class CreditRequested(models.Model):
	CREDIT_REQUEST_CHOICES = (
		(0, 'Applicant Only'),
		(1, 'Joint with Co-Applicant(s)'),
	)
	amt_requested = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
	term_requested = models.CharField(max_length=256, null=True, blank=True) # unsure of what this is going to be
	loan_type = models.CharField(max_length=256, null=True, blank=True) # will probably turn into a CHOICES field later
	market_survey = models.CharField(max_length=256, null=True, blank=True) # unsure of what this is going to be
	request_purpose = models.CharField(max_length=256, null=True, blank=True)
	app_no = models.IntegerField(null=True, blank=True)
	credit_request = models.IntegerField(
		choices = CREDIT_REQUEST_CHOICES,
		default = 0,
	)
	
class ApplicantInfo(models.Model):
	APPLICATION_CHOICES = (
		(0, 'Borrower'),
		(1, 'Guarantor'),
		(2, 'Cosigner'),
		(3, 'Grantor'),
		(4, 'Other'),
	)
	APPLICANT_CHOICES = (
		(0, 'Individual'),
		(1, 'Association'),
		(2, 'Proprietorship'),
		(3, 'Trust'),
		(4, 'Partnership'),
		(5, 'Gov\'t Entity'),
		(6, 'Corporation'),
		(7, 'LLC'),
		(8, 'Non-Profit'),
	)
	MARITAL_CHOICES = (
		(0, 'Married'),
		(1, 'Unmarried'),
		(2, 'Seperated'),
	)
	application_type = models.IntegerField(
		choices = APPLICATION_CHOICES,
		default = 0,
	)
	last_name = models.CharField(max_length=256, null=True, blank=True)
	first_name = models.CharField(max_length=256, null=True, blank=True)
	ssn = models.IntegerField(null=True, blank=True)
	tin_no = models.IntegerField(null=True, blank=True)
	assumed_business_names = models.CharField(max_length=256, null=True, blank=True) # unsure what to name this field
	filing_dates = models.DateField(default=timezone.now)
	filing_locations = models.CharField(max_length=256, null=True, blank=True) # will probably want this to be a foreign key
	dba = models.CharField(max_length=256, null=True, blank=True)
	individual_independent = models.BooleanField()
	individual_dependent = models.BooleanField()
	joint_dependent = models.BooleanField()
	marital_status = models.IntegerField(
		choices = MARITAL_CHOICES,
		default = 0,
	)
	address = models.CharField(max_length=256, null=True, blank=True) # might want this to be foreign key
	mailing_addr = models.CharField(max_length=256, null=True, blank=True)
	principal_office_addr = models.CharField(max_length=256, null=True, blank=True)
	orginizations_state = models.CharField(max_length=2, null=True, blank=True) # will probably change to CHOICES list
	applicant_type = models.IntegerField(
		choices = APPLICANT_CHOICES,
		default = 0,
	)
	
# this model is repeated in pdf form, may want a recursive relation
class CollateralSchedule(models.Model):
	OWN_STATUS_CHOICES = (
		(0, 'Purchase Money'),
		(1, 'Presently Owned'),
	)
	description = models.CharField(max_length=256, null=True, blank=True)
	value = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
	liens_total = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
	ownership_status = models.IntegerField(
		choices = OWN_STATUS_CHOICES,
		default=0,
	)
	creditor_name = models.CharField(max_length=256, null=True, blank=True) # may want this to be foreign key
	
# this model is repeated in pdf form, may want a recursive relation
class AssetSchedule(models.Model):
	description = models.CharField(max_length=256, null=True, blank=True)
	value = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
	debt_subject = models.BooleanField() # unsure of what this is going to be
	asset_total = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
	
# this model is repeated in pdf form, may want a recursive relation
class LiabilitySchedule(models.Model):
	description = models.CharField(max_length=256, null=True, blank=True)
	type = models.CharField(max_length=256, null=True, blank=True)
	current_bal = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
	liability_total = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
	
# this model is repeated in pdf form, may want a recursive relation
class ExpenseSchedule(models.Model):
	description = models.CharField(max_length=256, null=True, blank=True)
	type = models.CharField(max_length=256, null=True, blank=True)
	amount = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
	per = models.CharField(max_length=256, null=True, blank=True) # might want to be CHOICES field
	annualized_total = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)

# this model is repeated in pdf form, may want a recursive relation
class IncomeSchedule(models.Model):
	description = models.CharField(max_length=256, null=True, blank=True)
	type = models.CharField(max_length=256, null=True, blank=True)
	annualized_amount = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
	annualized_total = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
	
class FinanceSummary(models.Model):
	assets_total = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
	liabilities_total = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
	net_worth = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
	annual_income = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
	annual_expenses = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
	net_annual_cash_flow = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
	
class RelationshipInfo(models.Model):
	CUSTOMER_CHOICES = (
		(0, 'New Customer'),
		(1, 'Existing Customer'),
	)
	customer_type = models.IntegerField(
		choices = CUSTOMER_CHOICES,
		default = 0,
	)
	customer_since = models.IntegerField()
	last_tax_return = models.DateField(default=timezone.now)
	last_financial_statement = models.DateField(default=timezone.now)
	last_credit_report = models.DateField(default=timezone.now)
	last_credit_bureau = models.DateField(default=timezone.now)
	
	# below fields are a part of a subcategory called ("Liabilities with Lender")
	direct = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
	contingent = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
	total = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
	
	# below fields are a part of a subcategory called ("Deposits with Lender")
	dda_avg = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
	other_avg = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
	total_avg = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
	
	# below fields are a part of a subcategory called ("Deposits with Lender")
	new_credit = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
	proposed_total = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
		
class ApplicantSigners(models.Model):
	name = models.CharField(max_length=256, null=True, blank=True)
	title = models.CharField(max_length=256, null=True, blank=True)
	authorized = models.BooleanField()
	ssn = models.IntegerField(null=True, blank=True)
	address = models.CharField(max_length=256, null=True, blank=True)
	city = models.CharField(max_length=256, null=True, blank=True)
	state = models.CharField(max_length=256, null=True, blank=True)
	zip_code = models.IntegerField(null=True, blank=True)
	phone_number = models.CharField(max_length=256, null=True, blank=True)
	
class ApplicantSignatures(models.Model):
	applicant = models.ForeignKey(ApplicantSigners, null=True, blank=True)
	is_signed = models.BooleanField()
	
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
	officer_name = models.CharField(max_length=256, null=True, blank=True)
	officer_number = models.IntegerField(null=True, blank=True)
	approved_by = models.CharField(max_length=256, null=True, blank=True) # unsure of what this is going to be
	concurrence_by = models.CharField(max_length=256, null=True, blank=True) # unsure of what this is going to be
	committee_date = models.DateField(default=timezone.now)
	decision_date = models.DateField(default=timezone.now)
	branch = models.CharField(max_length=256, null=True, blank=True)
	app_date = models.DateField(default=timezone.now)
	app_number = models.IntegerField(null=True, blank=True)
	commitment_numbers = models.IntegerField(null=True, blank=True)
	loan_number = models.IntegerField(null=True, blank=True)
	mortgage_loan_originator_id = models.CharField(max_length=256, null=True, blank=True)
	mortgage_loan_company_id = models.CharField(max_length=256, null=True, blank=True)
	decision = models.IntegerField(
		choices = DECISION_CHOICES,
		default = 0,
	)