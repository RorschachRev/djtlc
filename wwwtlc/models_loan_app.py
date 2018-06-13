import datetime
from decimal import Decimal
from django.db import models
from django.utils import timezone

#*************************************************************************************************************************************
# v1.1 of models from Commercial_loan_app_transcript.txt														\
# Will need extensive modifying - possibly within the djtlc/loan/models.py file as well									\
# To be used in addition with models.loan_app2.py (seperated for pdf referencing purposes)								\
# 																									\
# In it's current state, most of the models have been merged into the models_loan_app2.py file							\
# many of the models have either been removed completely or they have been modified/moved							\
# to the other file. Now it's just a graveyard of old models only to be used as references until they						\
# meet their ultimate doom at the hands of me, the developer mwahahahaha											\
#*************************************************************************************************************************************

'''class CreditRequest(models.Model):
	CREDIT_REQUEST_CHOICES = (
		(0, 'Applicant Only'),
		(1, 'Joint with Co-Applicant(s)'),
	)
	amt_requested = models.DecimalField(max_digits=12, decimal_places=2)
	term_requested = models.CharField(max_length=256) # unsure of what this is going to be
	loan_type = models.CharField(max_length=256) # will probably turn into a CHOICES field later
	market_survey = models.CharField(max_length=256, null=True, blank=True) # unsure of what this is going to be
	request_purpose = models.TextField(null=True, blank=True)
	app_no = models.IntegerField()
	credit_request = models.IntegerField(
		choices = CREDIT_REQUEST_CHOICES,
		default = 0,
	)
	
# This model has been merged into models_loan_app2/BorrowerInfo
# it is commented out here for reference in case things go sour
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
	tin_no = models.IntegerField(null=True, blank=True)
	assumed_business_names = models.CharField(max_length=256, null=True, blank=True) # unsure what to name this field
	filing_dates = models.DateField(default=timezone.now)
	filing_locations = models.CharField(max_length=256, null=True, blank=True) # will probably want this to be a foreign key
	dba_name = models.CharField(max_length=256, null=True, blank=True)
	individual_independent = models.BooleanField()
	individual_dependent = models.BooleanField()
	joint_dependent = models.BooleanField()
	# this marital status is more flushed out, so will probably want to keep this one, not one in other model
	marital_status = models.IntegerField(
		choices = MARITAL_CHOICES,
		default = 0,
	)
	mailing_addr = models.CharField(max_length=256, null=True, blank=True)
	principal_office_addr = models.CharField(max_length=256, null=True, blank=True)
	orginizations_state = models.CharField(max_length=2, null=True, blank=True) # will probably change to CHOICES list
	applicant_type = models.IntegerField(
		choices = APPLICANT_CHOICES,
		default = 0,
	)
	#last_name = models.CharField(max_length=256, null=True, blank=True)
	#first_name = models.CharField(max_length=256, null=True, blank=True)
	#ssn = models.IntegerField(null=True, blank=True)
	#address = models.CharField(max_length=256, null=True, blank=True) # might want this to be foreign key
	
# this model is repeated in pdf form, may want relationship in a summary table
# also, not included in other model file, unsure what it would merge as though
# it may possibly turn into the commented out code in the Liability model
class CollateralSchedule(models.Model):
	OWN_STATUS_CHOICES = (
		(0, 'Purchase Money'),
		(1, 'Presently Owned'),
	)
	description = models.CharField(max_length=256)
	value = models.DecimalField(max_digits=12, decimal_places=2)
	liens_total = models.DecimalField(max_digits=12, decimal_places=2)
	ownership_status = models.IntegerField(
		choices = OWN_STATUS_CHOICES,
		default=0,
	)
	creditor_name = models.CharField(max_length=256, null=True, blank=True) # may want this to be foreign key to a 'Person' || 'Creditor' || 'Officer' table - unsure best approach
	
# this table is much more well documented in other models file (ALSummary), may want to 
# scrap this one, commented out for now, however, it does contain a couple
# fields that may need to be included, they are marked by the # comments
class FinanceSummary(models.Model):
	assets_total = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
	liabilities_total = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
	net_worth = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
	#annual_income = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
	#annual_expenses = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
	#net_annual_cash_flow = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
	
class RelationshipInfo(models.Model):
	CUSTOMER_CHOICES = (
		(0, 'New Customer'),
		(1, 'Existing Customer'),
	)
	customer_type = models.IntegerField(
		choices = CUSTOMER_CHOICES,
		default = 0,
	)
	customer_since = models.IntegerField(null=True, blank=True)
	last_tax_return = models.DateField(null=True, blank=True)
	last_financial_statement = models.DateField(null=True, blank=True)
	last_credit_report = models.DateField(null=True, blank=True)
	last_credit_bureau = models.DateField(null=True, blank=True)
	
	# below fields are a part of a subcategory called ("Liabilities with Lender")
	direct = models.DecimalField(max_digits=12, decimal_places=2)
	contingent = models.DecimalField(max_digits=12, decimal_places=2)
	total = models.DecimalField(max_digits=12, decimal_places=2)
	
	# below fields are a part of a subcategory called ("Deposits with Lender")
	dda_avg = models.DecimalField(max_digits=12, decimal_places=2)
	other_avg = models.DecimalField(max_digits=12, decimal_places=2)
	total_avg = models.DecimalField(max_digits=12, decimal_places=2)
	
	# below fields are a part of a subcategory called ("Deposits with Lender")
	new_credit = models.DecimalField(max_digits=12, decimal_places=2)
	proposed_total = models.DecimalField(max_digits=12, decimal_places=2)
	
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
	officer_name = models.CharField(max_length=256)
	officer_number = models.IntegerField()
	approved_by = models.CharField(max_length=256) # will probably turn into FK to a 'Person' || 'Creditor' || 'Officer table - unsure which would work best
	concurrence_by = models.CharField(max_length=256) # will probably turn into FK to a 'Person' || 'Creditor' || 'Officer table - unsure which would work best
	committee_date = models.DateField()
	decision_date = models.DateField()
	branch = models.CharField(max_length=256) # this could be an Address (?)
	app_date = models.DateField()
	app_number = models.IntegerField()
	commitment_number = models.IntegerField()
	loan_number = models.IntegerField()
	mortgage_loan_originator_id = models.CharField(max_length=256)# will probably turn into FK to a 'Person' || 'Creditor' || 'Officer table - unsure which would work best
	mortgage_loan_company_id = models.CharField(max_length=256) # will probably turn into FK - unsure to what table though, may need to make a new one
	decision = models.IntegerField(
		choices = DECISION_CHOICES,
		default = 0,
	)'''