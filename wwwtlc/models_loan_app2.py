import datetime
from decimal import Decimal
from django.db import models
from django.utils import timezone

# (SUPER)Rough Draft of models from Commercial_loan_app2_transcript.txt
# Will need extensive modifying - possibly within the djtlc/loan/models.py file as well
# To be used in addition with models.loan_app.py (seperated for pdf referencing purposes)

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
	agency_case_no = models.IntegerField(null=True, blank=True)
	lender_case_no = models.IntegerField(null=True, blank=True)
	loan_amount = models.DecimalField(max_digits=12, decimal_places=4, null=True, blank=True)
	int_rate = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)
	months = models.IntegerField(null=True, blank=True) #number of months - will need different name
	amortization_type = models.IntegerField(
		choices = AMORTIZATION_CHOICES,
		default = 0,
	)
	
class PropertyInfo (models.Model):
	address = models.CharField(max_length=256, null=True, blank=True) # will probably want to make this a foreign key relation
	no_units = models.IntegerField(null=True, blank=True) # number of units - will need different name
	legal_description = models.CharField(max_length=256, null=True, blank=True)
	year_built = models.IntegerField(null=True, blank=True)
	is_construction = models.BooleanField(default=False) # if True, will need to add: 	\
											  # year_acquired			\
											  # original_cost			\
											  # amount_existing_liens	\
											  # present_value			\
											  # improve_cost			\
											  # total (present + improve)	\
											  
	is_refinance = models.BooleanField(default=False) # if True, will need to add:		\
										     # year_acquired				\
										     # original_cost				\
										     # amount_existing_liens		\
										     # refinance_purpose			\
										     
	cost = models.DecimalField(max_digits=12, decimal_places=4, null=True, blank=True)
	title_names = models.CharField(max_length=256, null=True, blank=True) #will probably want a many-to-many relation
	
class BorrowerInfo (models.Model):
	borrower_name = models.CharField(max_length=256, null=True, blank=True)
	coborrower = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True) # recursive relationship
	ssn = models.IntegerField(null=True, blank=True)
	home_phone = models.CharField(max_length=256, null=True, blank=True)
	dob = models.DateField(default=timezone.now)
	yrs_school = models.IntegerField(null=True, blank=True) # years of schooling completed
	marriage_status = models.BooleanField()
	dependents = models.IntegerField(null=True, blank=True)
	present_addr = models.CharField(max_length=256, null=True, blank=True) # will probably be a foreign key
	own_rent = models.BooleanField() # may want to be a CHOICES field instead
	living_yrs = models.IntegerField() # years owned/rented at property referenced in present_addr
	mail_addr = models.CharField(max_length=256, null=True, blank=True)
	
	# below are fields to be filled out if own_rent < 2
	former_addr = models.CharField(max_length=256, null=True, blank=True)
	former_own_rent = models.BooleanField() # may wanto to be a CHOICES field instead
	former_lived_yrs = models.IntegerField(null=True, blank=True) # years owned/rented at property referenced \
								      # in former_addr
								      
class EmploymentInfo(models.Model):
	borrower = models.ForeignKey(BorrowerInfo, null=True, blank=True)
	name = models.CharField(max_length=256, null=True, blank=True)
	addr = models.CharField(max_length=256, null=True, blank=True) # will probably want to be a foreign key
	self_employed = models.BooleanField(default=False)
	yrs_worked = models.IntegerField(null=True, blank=True) # years worked at current employer
	yrs_in_profession = models.IntegerField(null=True, blank=True) # years worked in the related field
	position = models.CharField(max_length=256, null=True, blank=True)
	title = models.CharField(max_length=256, null=True, blank=True)
	business_type = models.CharField(max_length=256, null=True, blank=True)
	business_phone = models.CharField(max_length=256, null=True, blank=True)
	
	# if yrs_worked < 2 || if working in more than, one position 	\
	# the following fields will need to be created / filled out:		\
		# Employer Name								\
		# Employer Address							\
		# Self-Employed(?)								\
		# Employment Dates (from -to)					\
		# Monthly Income								\
		# Position									\
		# Title										\
		# Type of Business								\
		# Business Phone								\
		
class IncomeExpenseInfo(models.Model):
	borrower = models.ForeignKey(BorrowerInfo, null=True, blank=True)
	
	# below fields may need to be in another table (called Income), \
	# and then referenced to in this one
	base_empl_income = models.DecimalField(max_digits=12, decimal_places=4, null=True, blank=True)
	overtime = models.DecimalField(max_digits=12, decimal_places=4, null=True, blank=True)
	bonuses = models.DecimalField(max_digits=12, decimal_places=4, null=True, blank=True)
	commissions = models.DecimalField(max_digits=12, decimal_places=4, null=True, blank=True)
	dividends = models.DecimalField(max_digits=12, decimal_places=4, null=True, blank=True)
	interest = models.DecimalField(max_digits=12, decimal_places=4, null=True, blank=True)
	net_rental = models.DecimalField(max_digits=12, decimal_places=4, null=True, blank=True)
	income_other = models.DecimalField(max_digits=12, decimal_places=4, null=True, blank=True)
	income_total = models.DecimalField(max_digits=12, decimal_places=4, null=True, blank=True)
	
	# below fields may need to be in another table (called MonthlyHousingExpenses), \
	# and then referenced to in this one
	rent = models.DecimalField(max_digits=12, decimal_places=4, null=True, blank=True)
	first_mortgage = models.DecimalField(max_digits=12, decimal_places=4, null=True, blank=True)
	other_financing = models.DecimalField(max_digits=12, decimal_places=4, null=True, blank=True)
	hazard_insur = models.DecimalField(max_digits=12, decimal_places=4, null=True, blank=True)
	real_estate_taxes = models.DecimalField(max_digits=12, decimal_places=4, null=True, blank=True)
	mortgage_insur = models.DecimalField(max_digits=12, decimal_places=4, null=True, blank=True)
	expense_other = models.DecimalField(max_digits=12, decimal_places=4, null=True, blank=True)
	expense_total = models.DecimalField(max_digits=12, decimal_places=4, null=True, blank=True)
	
	# this next section is for describing other income	\
	# NOTICE: Alimony, child support, or seperate	\
	# maintenance income need not to be revealed	\
	
	# will also need to add the following fields either 	\
	# to this table or another one:					\
		# Borrower || Co-borrower				\
		# Description							\
		# Monthly Amount						\
		
class AssetsLiabilities(models.Model):
	jointly = models.BooleanField(default=False) # Are you filing jointly or not?
	
	# Assets block - may want to put in another table and have it referenced in this one
	description = models.CharField(max_length=256, null=True, blank=True)
	holding_deposit = models.CharField(max_length=256, null=True, blank=True) # unsure what this field is supposed 	\
											    # to be. on pdf, it just states:		\
											    # "Cash deposit toward purchase	\
											    # held by:" and then a blank area to 	\
											    # fill out. Could be a number, name,	\
											    # I don't know
	# below fields are for listing checking & savings accounts - may want to be a foreign key
	name = models.CharField(max_length=256, null=True, blank=True)
	acct_no = models.IntegerField(null=True, blank=True)
	amount = models.DecimalField(max_digits=12, decimal_places=4, null=True, blank=True)
	
	# below fields are for stocks and bonds - may want to be a foreign key
	stock_name = models.CharField(max_length=256, null=True, blank=True)
	stock_number = models.CharField(max_length=256, null=True, blank=True)
	stock_description = models.CharField(max_length=256, null=True, blank=True)
	bond_name = models.CharField(max_length=256, null=True, blank=True)
	bond_number = models.CharField(max_length=256, null=True, blank=True)
	bond_description = models.CharField(max_length=256, null=True, blank=True)
	
	life_insur_net = models.DecimalField(max_digits=12, decimal_places=4, null=True, blank=True)
	face_amount = models.DecimalField(max_digits=12, decimal_places=4, null=True, blank=True)
	subtotal_liquid = models.DecimalField(max_digits=12, decimal_places=4, null=True, blank=True)
	vested_interest = models.DecimalField(max_digits=12, decimal_places=4, null=True, blank=True)
	net_worth = models.DecimalField(max_digits=12, decimal_places=4, null=True, blank=True) # of business(es) owned
	
	# may want to make below fields a foreign key
	vehicle_make = models.CharField(max_length=256, null=True, blank=True)
	vehicle_model = models.CharField(max_length=256, null=True, blank=True)
	
	# assets_other - needs to be itemized (which makes me think that the assets section	\
	# should be a foreign key)
	assets_total = models.DecimalField(max_digits=12, decimal_places=4, null=True, blank=True)
	
	# Liabilities Block - may want to put in another table and have it referenced in this one
	company_name = models.CharField(max_length=256, null=True, blank=True)
	company_address = models.CharField(max_length=256, null=True, blank=True)
	monthly_payment = models.DecimalField(max_digits=12, decimal_places=4, null=True, blank=True)
	months_left = models.IntegerField(null=True, blank=True) # months left on monthly_payment
	unpaid_balance = models.DecimalField(max_digits=12, decimal_places=4, null=True, blank=True)
	acct_no = models.IntegerField(null=True, blank=True)
	
	alimony = models.BooleanField(default=False)
	alimony_owed = models.DecimalField(max_digits=12, decimal_places=4, null=True, blank=True)
	child_support = models.BooleanField(default=False)
	child_support_owed = models.DecimalField(max_digits=12, decimal_places=4, null=True, blank=True)
	seperate_maint = models.BooleanField(default=False)
	seperate_maint_owed = models.DecimalField(max_digits=12, decimal_places=4, null=True, blank=True)
	
	job_related_expenses = models.DecimalField(max_digits=12, decimal_places=4, null=True, blank=True)
	total_monthly_payments = models.DecimalField(max_digits=12, decimal_places=4, null=True, blank=True)
	liabilities_total = models.DecimalField(max_digits=12, decimal_places=4, null=True, blank=True)
	
	net_worth = models.DecimalField(max_digits=12, decimal_places=4, null=True, blank=True) # assests_total	\
														  # - liabilities_total	\
	real_estate_schedule = models.CharField(max_length=256, null=True, blank=True) # may want to be a CHOICES field
	property_address = models.CharField(max_length=256, null=True, blank=True)
	property_type = models.CharField(max_length=256, null=True, blank=True) # will want to be CHOICES field later
	present_market_value = models.DecimalField(max_digits=12, decimal_places=4, null=True, blank=True)
	mortgage_amt = models.DecimalField(max_digits=12, decimal_places=4, null=True, blank=True)
	liens_amt = models.DecimalField(max_digits=12, decimal_places=4, null=True, blank=True)
	gross_rental_income = models.DecimalField(max_digits=12, decimal_places=4, null=True, blank=True)
	mortgage_payments = models.DecimalField(max_digits=12, decimal_places=4, null=True, blank=True)
	misc_payments = models.DecimalField(max_digits=12, decimal_places=4, null=True, blank=True)
	net_rental_income = models.DecimalField(max_digits=12, decimal_places=4, null=True, blank=True)
	
	# totals # unsure of what this is going to be. in pdf it says:	\
		     # "Totals (fore each of the above categories NOT	\
		     # classified under Liabilities block"			
	
	# below fields are for listing any additional names under which credit has previously been recieved
	prev_alt_name = models.CharField(max_length=256, null=True, blank=True)
	prev_creditor_name = models.CharField(max_length=256, null=True, blank=True)
	prev_acct_no = models.IntegerField(null=True, blank=True)
	
#***********************************************************************************************
# "Details of Transaction" would go here, but on handwritten notes, it said "IAN FILTER"	\
# unsure whether or not this meant to Omit or not, so I left it out						\
#***********************************************************************************************

class Declarations(models.Model):
	borrower = models.ForeignKey(BorrowerInfo, null=True, blank=True)
	
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
	
	continuation = models.CharField(max_length=256, null=True, blank=True)
	
class AcknowledgeAgree(models.Model):
	borrower = models.ForeignKey(BorrowerInfo, null=True, blank=True)
	coborrower = models.ForeignKey(BorrowerInfo, null=True, blank=True)
	borrower_agree = models.BooleanField(default=False)
	coborrower_agree = models.BooleanField(default=False)
	date = models.DateField(default=timezone.now)
	