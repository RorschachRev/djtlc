import datetime
from decimal import Decimal
from django.db import models
from django.utils import timezone
from .models import Address

#*************************************************************************************************************************************
# v1.1 of models from Commercial_loan_app2_transcript.txt														\
# Will need extensive modifying - possibly within the djtlc/loan/models.py file as well									\
# To be used in addition with models.loan_app.py (seperated for pdf referencing purposes)								\
# 																									\
# In it's current state there are a lot of foreign key calls for information that may need filled out multiple times,				\
# may want to change this if there is a better way to handle that hierarchy											\
#*************************************************************************************************************************************
# commented out for now, causes conflicts with original models, but those files will eventually be removed, in which case this block will be uncommented and the import will be removed
'''class Address(models.Model):
	street1=models.CharField(max_length=254, help_text="The street address of the property needing financed", verbose_name="Street 1")
	street2=models.CharField(max_length=254, blank=True, verbose_name="Street 2", help_text="(optional)")
	street3=models.CharField(max_length=254, blank=True, verbose_name="Street 3", help_text="(optional)")
	city=models.CharField(max_length=127)
	state=models.CharField(max_length=25)
	zipcode=models.CharField(max_length=10)
	country	=models.CharField(max_length=3)
	
	def __str__(self):
		return self.street1'''

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
	)
	agency_case_no = models.IntegerField()
	lender_case_no = models.IntegerField()
	loan_amount = models.DecimalField(max_digits=12, decimal_places=4)
	int_rate = models.DecimalField(max_digits=4, decimal_places=2) # requested int_rate?
	months = models.IntegerField() #number of months - will need different name
	amortization_type = models.IntegerField(
		choices = AMORTIZATION_CHOICES,
		default = 0,
	)
		
class ConstructionInfo(models.Model):
	year_acquired = models.DateField(default=timezone.now)
	original_cost = models.DecimalField(max_digits=12, decimal_places=2)
	amt_existing_liens = models.DecimalField(max_digits=12, decimal_places=2)
	present_value = models.DecimalField(max_digits=12, decimal_places=2) # a.
	improve_cost = models.DecimalField(max_digits=12, decimal_places=2) # b.
	total = models.DecimalField(max_digits=12, decimal_places=2) # (a + b)
	
class RefinanceInfo(models.Model):
	year_acquired = models.DateField(default=timezone.now)
	original_cost = models.DecimalField(max_digits=12, decimal_places=2)
	amt_existing_liens = models.DecimalField(max_digits=12, decimal_places=2)
	refine_purpose = models.CharField(max_length=256)
	total_cost = models.DecimalField(max_digits=12, decimal_places=2)
	
class PropertyInfo (models.Model):
	address = models.ForeignKey(Address)
	no_units = models.IntegerField() # number of units - might need different name
	legal_description = models.CharField(max_length=256)
	year_built = models.IntegerField()
	construction_loan = models.ForeignKey(ConstructionInfo, null=True, blank=True)
	refinance_loan = models.ForeignKey(RefinanceInfo, null=True, blank=True)
	title_names = models.CharField(max_length=256, null=True, blank=True) #will probably want a many-to-many relation - unsure if should be linked to BorrowerInfo or not
								      
class EmploymentInfo(models.Model):
	name = models.CharField(max_length=256)
	address = models.ForeignKey(Address)
	self_employed = models.BooleanField(default=False)
	yrs_worked = models.IntegerField() # years worked at current employer
	yrs_in_profession = models.IntegerField() # years worked in the related field
	position = models.CharField(max_length=256)
	title = models.CharField(max_length=256)
	business_type = models.CharField(max_length=256)
	business_phone = models.CharField(max_length=256)
	
	# if yrs_worked < 2 || if working in more than one position, 	\
	# the following fields will need to be created / filled out:		\
	other_emp_info = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
	
class IncomeInfo(models.Model):
	base_empl_income = models.DecimalField(max_digits=12, decimal_places=4)
	overtime = models.DecimalField(max_digits=12, decimal_places=4, null=True, blank=True)
	bonuses = models.DecimalField(max_digits=12, decimal_places=4, null=True, blank=True)
	commissions = models.DecimalField(max_digits=12, decimal_places=4, null=True, blank=True)
	dividends = models.DecimalField(max_digits=12, decimal_places=4, null=True, blank=True)
	interest = models.DecimalField(max_digits=12, decimal_places=4, null=True, blank=True)
	net_rental = models.DecimalField(max_digits=12, decimal_places=4, null=True, blank=True)
	other_description = models.TextField(null=True, blank=True)
	income_other = models.DecimalField(max_digits=12, decimal_places=4, null=True, blank=True)
	income_total = models.DecimalField(max_digits=12, decimal_places=4)
	
class ExpenseInfo(models.Model):
	rent = models.DecimalField(max_digits=12, decimal_places=4, null=True, blank=True)
	first_mortgage = models.DecimalField(max_digits=12, decimal_places=4, null=True, blank=True)
	other_financing = models.DecimalField(max_digits=12, decimal_places=4, null=True, blank=True)
	hazard_insur = models.DecimalField(max_digits=12, decimal_places=4, null=True, blank=True)
	real_estate_taxes = models.DecimalField(max_digits=12, decimal_places=4, null=True, blank=True)
	mortgage_insur = models.DecimalField(max_digits=12, decimal_places=4, null=True, blank=True)
	other_description = models.TextField(null=True, blank=True)
	expense_other = models.DecimalField(max_digits=12, decimal_places=4, null=True, blank=True)
	expense_total = models.DecimalField(max_digits=12, decimal_places=4)
	
class BankAccount(models.Model):
	name = models.CharField(max_length=256)
	acct_no = models.IntegerField()
	amount = models.DecimalField(max_digits=12, decimal_places=4)
	
class Stock(models.Model):
	stock_name = models.CharField(max_length=256)
	stock_number = models.CharField(max_length=256)
	stock_description = models.TextField()
	stock_amount = models.DecimalField(max_digits=12, decimal_places=2)
	
class Bond(models.Model):
	bond_name = models.CharField(max_length=256)
	bond_number = models.CharField(max_length=256)
	bond_description = models.TextField()
	bond_amount = models.DecimalField(max_digits=12, decimal_places=2)
	
class Vehicle(models.Model):
	vehicle_make = models.CharField(max_length=256)
	vehicle_model = models.CharField(max_length=256)
	vehicle_amount = models.DecimalField(max_digits=12, decimal_places=2)
	
class AssetSummary(models.Model):
	holding_deposit = models.CharField(max_length=256, null=True, blank=True) # unsure what this field is supposed 	\
															       # to be. on pdf, it just states:			\
															       # "Cash deposit toward purchase		\
															       # held by:" and then a blank area to 	\
															       # fill out. Could be a number, name,		\
															       # I don't know
	# below fields are for listing checking & savings accounts
	acct1 = models.ForeignKey(BankAccount, related_name='acc_1')
	acct2 = models.ForeignKey(BankAccount, related_name='acc_2', null=True, blank=True)
	acct3 = models.ForeignKey(BankAccount, related_name='acc_3', null=True, blank=True)
	
	# below fields are for stocks
	stock1 = models.ForeignKey(Stock, related_name='stock_1', null=True, blank=True)
	stock2 = models.ForeignKey(Stock, related_name='stock_2', null=True, blank=True)
	stock3 = models.ForeignKey(Stock, related_name='stock_3', null=True, blank=True)
	stock4 = models.ForeignKey(Stock, related_name='stock_4', null=True, blank=True)
	stock5 = models.ForeignKey(Stock, related_name='stock_5', null=True, blank=True)
	
	# below fields are for bonds
	bond1 = models.ForeignKey(Bond, related_name='bond_1', null=True, blank=True)
	bond2 = models.ForeignKey(Bond, related_name='bond_2', null=True, blank=True)
	bond3 = models.ForeignKey(Bond, related_name='bond_3', null=True, blank=True)
	bond4 = models.ForeignKey(Bond, related_name='bond_4', null=True, blank=True)
	bond5 = models.ForeignKey(Bond, related_name='bond_5', null=True, blank=True)
	
	life_insur_net = models.DecimalField(max_digits=12, decimal_places=4, null=True, blank=True)
	face_amount = models.DecimalField(max_digits=12, decimal_places=4, null=True, blank=True)
	subtotal_liquid = models.DecimalField(max_digits=12, decimal_places=4)
	vested_interest = models.DecimalField(max_digits=12, decimal_places=4, null=True, blank=True)
	net_worth = models.DecimalField(max_digits=12, decimal_places=4, null=True, blank=True) # of business(es) owned
	
	vehicle1 = models.ForeignKey(Vehicle, related_name='vehicle_1', null=True, blank=True)
	vehicle2 = models.ForeignKey(Vehicle, related_name='vehicle_2', null=True, blank=True)
	vehicle3 = models.ForeignKey(Vehicle, related_name='vehicle_3', null=True, blank=True)
	vehicle4 = models.ForeignKey(Vehicle, related_name='vehicle_4', null=True, blank=True)
	vehicle5 = models.ForeignKey(Vehicle, related_name='vehicle_5', null=True, blank=True)
	
	other_description = models.TextField(null=True, blank=True)
	other_amt_total = models.DecimalField(max_digits=12, decimal_places=2)
	
	assets_total = models.DecimalField(max_digits=12, decimal_places=4)
	
class Debt(models.Model):
	company_name = models.CharField(max_length=256)
	acct_no = models.IntegerField()
	company_address = models.CharField(max_length=256)
	monthly_payment = models.DecimalField(max_digits=12, decimal_places=4)
	months_left = models.IntegerField() # months left on monthly_payment
	unpaid_balance = models.DecimalField(max_digits=12, decimal_places=4)
	
class Alimony(models.Model):
	owed_to = models.CharField(max_length=256)
	amt_owed = models.DecimalField(max_digits=12, decimal_places=4)
	
class ChildSupport(models.Model):
	owed_to = models.CharField(max_length=256)
	amt_owed = models.DecimalField(max_digits=12, decimal_places=4)
	
class SeparateMaint(models.Model):
	owed_to = models.CharField(max_length=256)
	amt_owed = models.DecimalField(max_digits=12, decimal_places=4)
	
class LiabilitySummary(models.Model):
	debt1 = models.ForeignKey(Debt, related_name='debt1', null=True, blank=True)
	debt2 = models.ForeignKey(Debt, related_name='debt2', null=True, blank=True)
	debt3 = models.ForeignKey(Debt, related_name='debt3', null=True, blank=True)
	debt4 = models.ForeignKey(Debt, related_name='debt4', null=True, blank=True)
	debt5 = models.ForeignKey(Debt, related_name='debt5', null=True, blank=True)
	debt6 = models.ForeignKey(Debt, related_name='debt6', null=True, blank=True)
	
	alimony1 = models.ForeignKey(Alimony, related_name='alimony1', null=True, blank=True)
	alimony2 = models.ForeignKey(Alimony, related_name='alimony2', null=True, blank=True)
	alimony3 = models.ForeignKey(Alimony, related_name='alimony3', null=True, blank=True)
	
	child_supp1 = models.ForeignKey(ChildSupport, related_name='child_supp1', null=True, blank=True)
	child_supp2 = models.ForeignKey(ChildSupport, related_name='child_supp2', null=True, blank=True)
	child_supp3 = models.ForeignKey(ChildSupport, related_name='child_supp3', null=True, blank=True)
	
	separate_maint1 = models.ForeignKey(SeparateMaint, related_name='sep_maint1', null=True, blank=True)
	separate_maint2 = models.ForeignKey(SeparateMaint, related_name='sep_maint2', null=True, blank=True)
	separate_maint3 = models.ForeignKey(SeparateMaint, related_name='sep_maint3', null=True, blank=True)
	
	job_related_expenses = models.DecimalField(max_digits=12, decimal_places=4, null=True, blank=True)
	
	total_monthly_payments = models.DecimalField(max_digits=12, decimal_places=4)
	liabilities_total = models.DecimalField(max_digits=12, decimal_places=4)
	
	# Unsure what to do with this code, my intuition says to make it a FK, 	\
	# however,  I'm unsure if it will be classified as Asset or Liability
	'''real_estate_schedule = models.CharField(max_length=256, null=True, blank=True) # may want to be a CHOICES field
	property_address = models.CharField(max_length=256, null=True, blank=True)
	property_type = models.CharField(max_length=256, null=True, blank=True) # will want to be CHOICES field later
	present_market_value = models.DecimalField(max_digits=12, decimal_places=4, null=True, blank=True)
	mortgage_amt = models.DecimalField(max_digits=12, decimal_places=4, null=True, blank=True)
	liens_amt = models.DecimalField(max_digits=12, decimal_places=4, null=True, blank=True)
	gross_rental_income = models.DecimalField(max_digits=12, decimal_places=4, null=True, blank=True)
	mortgage_payments = models.DecimalField(max_digits=12, decimal_places=4, null=True, blank=True)
	misc_payments = models.DecimalField(max_digits=12, decimal_places=4, null=True, blank=True)
	net_rental_income = models.DecimalField(max_digits=12, decimal_places=4, null=True, blank=True)'''
	
	# totals # unsure of what this is going to be. in pdf it says:	\
		     # "Totals (for each of the above categories NOT	\
		     # classified under Liabilities block"			
	
class ALSummary(models.Model):
	jointly = models.BooleanField(default=False) # Are you filing jointly or not?
	assets = models.ForeignKey(AssetSummary)
	liabilities = models.ForeignKey(LiabilitySummary)
	net_worth = models.DecimalField(max_digits=12, decimal_places=4, null=True, blank=True) # assests_total	\
																		      # - liabilities_total	\
	
	# below fields are for listing any additional names under which credit has previously been recieved
	prev_alt_name = models.CharField(max_length=256, null=True, blank=True)
	prev_creditor_name = models.CharField(max_length=256, null=True, blank=True)
	prev_acct_no = models.IntegerField(null=True, blank=True)
	
#***********************************************************************************************
# "Details of Transaction" would go here, but on handwritten notes, it said "IAN FILTER"	\
# unsure whether or not this meant to Omit or not, so I left it out						\
#***********************************************************************************************

class Declaration(models.Model):
	# on pdf, it states: "If 'Yes' to any questions a-i, use continuation sheet for explanation"	\
	# I put a textbox in this model to satisfy this requirement
	
	outstanding_judgements = models.BooleanField(default=False) # a.
	bankrupt = models.BooleanField(default=False) # b.
	forclosed = models.BooleanField(default=False) # c.
	lawsuit = models.BooleanField(default=False) # d.
	obligated_forclosure = models.BooleanField(default=False) # e. - "Have you directly or 	\
												 # indirectly been obligated	\
												 # on any loan which resulted	\
												 # in foreclosure, transfer of 	\
												 # title in lieu of foreclosure,	\
												 # or judgement?
	delinquent = models.BooleanField(default=False) # f. 1/2
	in_default = models.BooleanField(default=False) # f. 2/2
	alimony = models.BooleanField(default=False) # g. 1/3
	child_support = models.BooleanField(default=False) # g. 2/3
	seperate_maintenance = models.BooleanField(default=False) # g. 3/3
	borrowed_down_payment = models.BooleanField(default=False) # h.
	co_maker = models.BooleanField(default=False) # i. 1/2
	endorser = models.BooleanField(default=False) # i. 2/2
	
	us_citizen = models.BooleanField(default=False) # j.
	permanent_res_alien = models.BooleanField(default=False) # k.
	primary_residence = models.BooleanField(default=False) # l. - "Do you intend to occupy the	\
											      # property as your primary residence?"
	# ownership_interest in the last 3 years		\
	# if True, will need to add:				\
		# type_property_owned # CHOICE field	\
		# title_held_method # CHOICE field	\
	ownership_interest = models.BooleanField(default=False) # m.
	
	continuation = models.TextField(null=True, blank=True)
	
class BorrowerInfo (models.Model):
	OWN_RENT_CHOICES = (
		(0, 'Own'),
		(1, 'Rent'),
	)
	# TODO: Fix this ugly thing below
	OWN_RENT_CHOICES_NULL = (
		(0, 'Own'),
		(1, 'Rent'),
		(2, 'N/a'),
	)
	BORROWER_CHOICES = (
		(0, 'Borrower'),
		(1, 'Co-Borrower'),
	)
	borrower_fname = models.CharField(max_length=256)
	borrower_lname = models.CharField(max_length=256)
	borrower_type = models.IntegerField(
		choices = BORROWER_CHOICES,
		default = 0,
	)
	ssn = models.IntegerField()
	home_phone = models.CharField(max_length=256)
	dob = models.DateField(default=timezone.now)
	yrs_school = models.IntegerField() # years of schooling completed
	marriage_status = models.BooleanField()
	dependents = models.IntegerField()
	present_addr = models.ForeignKey(Address, related_name='present_addr')
	own_rent = models.IntegerField(
		choices = OWN_RENT_CHOICES,
		default = 0,
	)
	living_yrs = models.IntegerField() # years owned/rented at property referenced in present_addr
	mail_addr = models.CharField(max_length=256)
	
	# below are fields to be filled out if own_rent < 2
	former_addr = models.ForeignKey(Address, related_name='former_addr', null=True, blank=True)
	former_own_rent = models.IntegerField(
		choices = OWN_RENT_CHOICES_NULL,
		default = 2,
	)
	former_lived_yrs = models.IntegerField(null=True, blank=True) # years owned/rented at property referenced \
								# in former_addr
	employment = models.ForeignKey(EmploymentInfo)
	income = models.ForeignKey(IncomeInfo)
	expenses = models.ForeignKey(ExpenseInfo)
	assets = models.ForeignKey(ALSummary)
	declarations = models.ForeignKey(Declaration)
	
class AcknowledgeAgree(models.Model):
	borrower = models.ForeignKey(BorrowerInfo, related_name='borrower_agree', null=True, blank=True)
	borrower_agree = models.BooleanField(default=False)
	coborrower = models.ForeignKey(BorrowerInfo, related_name='coborrower_agree', null=True, blank=True)
	coborrower_agree = models.BooleanField(default=False)
	date = models.DateField(default=timezone.now)
	