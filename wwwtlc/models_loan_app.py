import datetime
from decimal import Decimal
from django.db import models
from django.utils import timezone
from .models import Address
from django.contrib.auth.models import User

#*************************************************************************************************************************************
# v1.3 - Current																						\
#																									\
#of models from Commercial_loan_app2_transcript.txt															\
# Will need extensive modifying - possibly within the djtlc/loan/models.py file as well									\
# To be used in addition with models.loan_app.py (seperated for pdf referencing purposes)								\
# 																									\
# v1.1																								\
# In it's current state there are a lot of foreign key calls for information that may need filled out multiple times,				\
# may want to change this if there is a better way to handle that hierarchy											\
# 																									\
# v1.2																								\
# The process of merging over the other models_loan_app.py models has begun, so there is a lot of refactoring				\
# to take care of. Most things will still need to be renamed and modified/moved around.								\
#																									\
# v1.3																								\
# Most models from the models_loan_app.py file have been moved over, and integrated									\
# There is a small (2) exception to this though, where I don't know where the models are goint to fit in						\
# Also, this is at the point where I need Ian to look through it so that we can discuss what stays and what					\
# goes																								\
#																									\
# v1.4																								\
# Changed a lot of models, renamed a few, moved some around. General revisioning. Created Loan Workflow model, as well		\
# as a TransactionDetails model that will need to be looked over, some fields might need removed, some might get to stay.		\
# 																									\
# Also, this version, I modified the wwwtlc/admin.py, wwwtlc/views.py, wwwtlc/urls.py, and the templates/pages/tier1_app.html	\
# && tier2_app.html to match the changes that I made in the models. The views and templates should correctly display each	\
# tiered application correctly with headings attached to them so that the user can know what section of the form they are on.	\
# Because the forms aren't in their final form (ha), many of the models necessitated null=True, blank=True (Especially all of the	\
# FK's) but when I start implementing the FormWizard form for these applications, this won't be necissary, as I will just tie all	\
# of the FK's in the view, like I did for the old loan application													\
#																									\
# In these models, you will also want to put -> , help_text='(required)'      anywhere that the field doesn't have				\
#																		null=True, blank=True			\
#																									\
# It's super tedious, and annoying, I know, but when you go to fill out the form, it will help you out a lot by being				\
# able to see which fields are required and to enter only those if you're testing whether or not the thing hits the db			\
# Along those same lines, if the Tier 2 application actually fills out the database, then the Tier 1 probably won't need tested	\
# as the view has the same syntax, and all of the Tier 1 ModelForms are included in the Tier 2 ModelForms					\
#																									\
# Any issues should be rather small, and confined within the models.py file as comments. There was some light confusion on	\
# some of the models, but for the most part, it is pretty much to the point that it needs to be at. Of course there will be some	\
# minor modifications, mostly to max_length properties of CharField fields, and some CHOICES fields, but all are minor, and can	\
# be fixed easily. The forms still need quite a bit of work, but in this generation, they should be presentable. No work has begun	\
# on customizing DjangoAdmin.																			\
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
	int_rate = models.DecimalField(max_digits=4, decimal_places=2)
	months_left = models.IntegerField()
	amortization_type = models.IntegerField(
		choices = AMORTIZATION_CHOICES,
		default = 0,
	)
		
# Added null=True & blank=True to both ConstructionInfo	\
# and RefinanceInfo models so that the form doesn't require 	\
# them. Will want to change this later on the next revision of	\
# the form. If CI || RI is_applicable, display forms, else don't	\
# kinda thing where the forms will require information if theyre displayed
class ConstructionInfo(models.Model):
	year_acquired = models.DateField(default=timezone.now, null=True, blank=True)
	original_cost = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
	amt_existing_liens = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
	present_value = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True) # a.
	improve_cost = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True) # b.
	total = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True) # (a + b)
	
class RefinanceInfo(models.Model):
	year_acquired = models.DateField(default=timezone.now, null=True, blank=True)
	original_cost = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
	amt_existing_liens = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
	refine_purpose = models.CharField(max_length=256, null=True, blank=True)
	total_cost = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
	
class PropertyInfo (models.Model):
	address = models.ForeignKey(Address, null=True, blank=True)
	no_units = models.IntegerField() # number of units
	legal_description = models.CharField(max_length=256)
	year_built = models.IntegerField()
	construction_loan = models.ForeignKey(ConstructionInfo, null=True, blank=True)
	refinance_loan = models.ForeignKey(RefinanceInfo, null=True, blank=True)
	title_names = models.CharField(max_length=256, null=True, blank=True) #will probably want a many-to-many relation - unsure if should be linked to BorrowerInfo or not
								      
class EmploymentIncome(models.Model): # for Tier 2, when personal income is needed for the application
	name = models.CharField(max_length=256, null=True, blank=True)
	address = models.ForeignKey(Address, null=True, blank=True)
	self_employed = models.BooleanField(default=False)
	yrs_worked = models.IntegerField(null=True, blank=True) # years worked at current employer
	yrs_in_profession = models.IntegerField(null=True, blank=True) # years worked in the related field
	position = models.CharField(max_length=256, null=True, blank=True)
	title = models.CharField(max_length=256, null=True, blank=True)
	business_type = models.CharField(max_length=256, null=True, blank=True)
	business_phone = models.CharField(max_length=256, null=True, blank=True)
	income = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True) # yearly amt
	
	# if yrs_worked < 2 || if working in more than one position, 	\
	# the following fields will need to be created / filled out:		\
	other_emp_info = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True) # recursive relationship
	
class BusinessInfo(models.Model):
	bus_name = models.CharField(max_length=256)
	bus_description = models.TextField()
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
	base_empl_income = models.DecimalField(max_digits=12, decimal_places=4)
	overtime = models.DecimalField(max_digits=12, decimal_places=4, null=True, blank=True)
	bonuses = models.DecimalField(max_digits=12, decimal_places=4, null=True, blank=True)
	commissions = models.DecimalField(max_digits=12, decimal_places=4, null=True, blank=True)
	other_description = models.TextField(null=True, blank=True)
	expense_other = models.DecimalField(max_digits=12, decimal_places=4, null=True, blank=True)
	expense_total = models.DecimalField(max_digits=12, decimal_places=4)
	
class BankAccount(models.Model):
	name = models.CharField(max_length=256, null=True, blank=True)
	acct_no = models.IntegerField(null=True, blank=True)
	amount = models.DecimalField(max_digits=12, decimal_places=4, null=True, blank=True)
	
class Stock(models.Model):
	stock_name = models.CharField(max_length=256, null=True, blank=True)
	stock_number = models.CharField(max_length=256, null=True, blank=True)
	stock_description = models.TextField(null=True, blank=True)
	stock_amount = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
	
class Bond(models.Model):
	bond_name = models.CharField(max_length=256, null=True, blank=True)
	bond_number = models.CharField(max_length=256, null=True, blank=True)
	bond_description = models.TextField(null=True, blank=True)
	bond_amount = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
	
class Vehicle(models.Model):
	vehicle_make = models.CharField(max_length=256, null=True, blank=True)
	vehicle_model = models.CharField(max_length=256, null=True, blank=True)
	vehicle_amount = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
	
class AssetSummary(models.Model):
	holding_deposit = models.CharField(max_length=256, null=True, blank=True) # unsure what this field is supposed 	\
															       # to be. on pdf, it just states:			\
															       # "Cash deposit toward purchase		\
															       # held by:" and then a blank area to 	\
															       # fill out. Could be who is holding the	\
															       # deposit, or the deposit amount, I don't	\
															       # know
	# below fields are for listing checking & savings accounts
	acct1 = models.ForeignKey(BankAccount, related_name='acc_1', null=True, blank=True)
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
	
	employment_income = models.ForeignKey(EmploymentIncome, null=True, blank=True)
	
	other_description = models.TextField(null=True, blank=True)
	other_amt_total = models.DecimalField(max_digits=12, decimal_places=2)
	
	assets_total = models.DecimalField(max_digits=12, decimal_places=4)
	
class Debt(models.Model):
	company_name = models.CharField(max_length=256, null=True, blank=True)
	acct_no = models.IntegerField(null=True, blank=True)
	company_address = models.CharField(max_length=256, null=True, blank=True)
	monthly_payment = models.DecimalField(max_digits=12, decimal_places=4, null=True, blank=True)
	months_left = models.IntegerField(null=True, blank=True) # months left on monthly_payment
	unpaid_balance = models.DecimalField(max_digits=12, decimal_places=4, null=True, blank=True)
	
class Alimony(models.Model):
	owed_to = models.CharField(max_length=256, null=True, blank=True)
	amt_owed = models.DecimalField(max_digits=12, decimal_places=4, null=True, blank=True)
	
class ChildSupport(models.Model):
	owed_to = models.CharField(max_length=256, null=True, blank=True)
	amt_owed = models.DecimalField(max_digits=12, decimal_places=4, null=True, blank=True)
	
class SeparateMaint(models.Model):
	owed_to = models.CharField(max_length=256, null=True, blank=True)
	amt_owed = models.DecimalField(max_digits=12, decimal_places=4, null=True, blank=True)
	
# previously in Liability summary block, unsure if this should go into the liability summary or the asset summary as a FK
class ManagedProperty(models.Model):
	real_estate_schedule = models.CharField(max_length=256, null=True, blank=True) # may want to be a CHOICES field
	property_address = models.ForeignKey(Address, null=True, blank=True)
	property_type = models.CharField(max_length=256, null=True, blank=True) # will want to be CHOICES field
	present_market_value = models.DecimalField(max_digits=12, decimal_places=4, null=True, blank=True)
	mortgage_amt = models.DecimalField(max_digits=12, decimal_places=4, null=True, blank=True)
	liens_amt = models.DecimalField(max_digits=12, decimal_places=4, null=True, blank=True)
	gross_rental_income = models.DecimalField(max_digits=12, decimal_places=4, null=True, blank=True) # might want to require this
	mortgage_payments = models.DecimalField(max_digits=12, decimal_places=4, null=True, blank=True)
	misc_payments = models.DecimalField(max_digits=12, decimal_places=4, null=True, blank=True) # might want to require this
	net_rental_income = models.DecimalField(max_digits=12, decimal_places=4, null=True, blank=True) # might want to require this
	
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
	
class ALSummary(models.Model):
	joint = models.BooleanField(default=False) # Are you filing jointly or not?
	assets = models.ForeignKey(AssetSummary, null=True, blank=True)
	liabilities = models.ForeignKey(LiabilitySummary, null=True, blank=True)
	net_worth = models.DecimalField(max_digits=12, decimal_places=4, null=True, blank=True) # assests_total	\
																		      # - liabilities_total	\
	annual_income = models.DecimalField(max_digits=12, decimal_places=2)
	annual_expenses = models.DecimalField(max_digits=12, decimal_places=2)
	net_annual_cash_flow = models.DecimalField(max_digits=12, decimal_places=2)
	
	# below fields are for listing any additional names under which credit has previously been recieved
	prev_alt_name = models.CharField(max_length=256, null=True, blank=True)
	prev_creditor_name = models.CharField(max_length=256, null=True, blank=True)
	prev_acct_no = models.IntegerField(null=True, blank=True)
	
#***********************************************************************************************
# "Details of Transaction" -> SECTION VII/commercial_loan_app2.pdf					\
# will go here, but it will require some modification by Ian, is also part of officer workflow	\
# A lot of these fields have long names, I just briefly ran through it, so I didn't think of		\
# any good names to condense the field titles a bit more than they are					\
#***********************************************************************************************
class TransactionDetails(models.Model):
	purchase_price = models.DecimalField(max_digits=12, decimal_places=2) # a.
	alterations = models.DecimalField(max_digits=12, decimal_places=2) # b. 1/3
	improvements = models.DecimalField(max_digits=12, decimal_places=2) # b. 2/3
	repairs = models.DecimalField(max_digits=12, decimal_places=2) # b. 3/3
	land = models.DecimalField(max_digits=12, decimal_places=2) # c. # if acquired seperately
	refinance = models.DecimalField(max_digits=12, decimal_places=2) # d. # including debts to be paid off
	estimated_prepaid_items = models.DecimalField(max_digits=12, decimal_places=2) # e.
	estimated_closing_costs = models.DecimalField(max_digits=12, decimal_places=2) # f.
	pmi = models.DecimalField(max_digits=12, decimal_places=2) # g. 1/3
	mip = models.DecimalField(max_digits=12, decimal_places=2) # g. 2/3
	funding_fee = models.DecimalField(max_digits=12, decimal_places=2) # g. 3/3
	discount = models.DecimalField(max_digits=12, decimal_places=2) # h.
	total_costs = models.DecimalField(max_digits=12, decimal_places=2) # i. # add items a through h
	subordinate_financing = models.DecimalField(max_digits=12, decimal_places=2) # j.
	closing_cost_paid = models.DecimalField(max_digits=12, decimal_places=2) # k. # "Borrower's closing costs paid by Seller"
	other_credits_description = models.TextField(null=True, blank=True) # l. 1/2
	other_credits_total = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True) # l. 2/2
	loan_amount_exclude = models.DecimalField(max_digits=12, decimal_places=2) # m. # exclude PMI, MIP, Funding Fee financed
	financed_pmi = models.DecimalField(max_digits=12, decimal_places=2) # n. 1/3
	financed_mip = models.DecimalField(max_digits=12, decimal_places=2) # n. 2/3
	financed_funding_fee = models.DecimalField(max_digits=12, decimal_places=2) # n. 3/3
	loan_amount = models.DecimalField(max_digits=12, decimal_places=2) # o. # add m. & n.
	borrower_cash = models.DecimalField(max_digits=12, decimal_places=2) # p. # "Cash from/to Borrower (subtract j, k, l & o from i)

class Declaration(models.Model):
	# on pdf, it states: "If 'Yes' to any questions a-i, use continuation sheet for explanation"	\
	# I put a textbox in this model to satisfy this requirement
	
	PROPERTY_TYPE_CHOICES = (
		(0, 'PR'),
		(1, 'SH'),
		(2, 'IP'),
	)
	TITLE_METHOD_CHOICES = (
		(0, 'S'),
		(1, 'SP'),
		(2, 'O'),
	)
	
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
	
	continuation = models.TextField(null=True, blank=True)
	
	# ownership_interest in the last 3 years		\
	# if True, user will need to fill out below fields
	
	ownership_interest = models.BooleanField(default=False) # m. 1/3
	
	m_property_type = models.IntegerField(
		choices = PROPERTY_TYPE_CHOICES,
		default = 0,
	)# m. 2/3 # on pdf, it says "What type of property did	\
			# you own--principal residence (PR), second	\
			# home (SH), or investment property (IP)?	\
			# will probably just specify this in help_text later
			
	m_title_method = models.IntegerField(
		choices = TITLE_METHOD_CHOICES,
		default = 0,
	)# m 3/3 # there should be a better name for this field	\
			# on pdf, it says, "How did you hold title to 	\
			# the home -- solely by yourself (S), jointly 	\
			#with your spouse (SP), or jointly with 		\
			# another person (O)?"					\
			# will probably just specify this in help_text later
	
class BorrowerInfo (models.Model):
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
	BORROWER_CHOICES = (
		(0, 'Borrower'),
		(1, 'Co-Borrower'),
	)
	FILING_CHOICES = (
		(0, 'Individual Independent'),
		(1, 'Individual Dependent'),
		(2, 'Joint'),
	)
	MARITAL_CHOICES = (
		(0, 'Married'),
		(1, 'Unmarried'),
		(2, 'Seperated'),
	)
	OWN_RENT_CHOICES = (
		(0, 'Own'),
		(1, 'Rent'),
	)
	OWN_RENT_CHOICES_NULL = (
		(0, 'Own'),
		(1, 'Rent'),
		(2, 'N/a'),
	)
	STATE_CHOICES = (
		(0, 'AL'),
		(1, 'AK'),
		(2, 'AZ'),
		(3, 'AR'),
		(4, 'CA'),
		(5, 'CO'),
		(6, 'CT'),
		(7, 'DE'),
		(8, 'DC'),
		(9, 'FL'),
		(10, 'GA'),
		(11, 'HI'),
		(12, 'ID'),
		(13, 'IL'),
		(14, 'IN'),
		(15, 'IA'),
		(16, 'KS'),
		(17, 'KY'),
		(18, 'LA'),
		(19, 'ME'),
		(20, 'MD'),
		(21, 'MA'),
		(22, 'MI'),
		(23, 'MN'),
		(24, 'MS'),
		(25, 'MO'),
		(26, 'MT'),
		(27, 'NE'),
		(28, 'NV'),
		(29, 'NH'),
		(30, 'NJ'),
		(31, 'NM'),
		(32, 'NY'),
		(33, 'NC'),
		(34, 'ND'),
		(35, 'OH'),
		(36, 'OK'),
		(37, 'OR'),
		(38, 'PA'),
		(39, 'RI'),
		(40, 'SC'),
		(41, 'SD'),
		(42, 'TN'),
		(43, 'TX'),
		(44, 'VT'),
		(45, 'VA'),
		(46, 'WA'),
		(47, 'WV'),
		(48, 'WI'),
		(49, 'WY'),
	)
		
	application_type = models.IntegerField(
		choices = APPLICATION_CHOICES,
		default = 0,
	)
	borrower_fname = models.CharField(max_length=256)
	borrower_lname = models.CharField(max_length=256)
	applicant_type = models.IntegerField(
		choices = APPLICANT_CHOICES,
		default = 0,
	)
	filing_type = models.IntegerField(
		choices = FILING_CHOICES,
		default = 0,
	)
	assumed_business_names = models.CharField(max_length=256, null=True, blank=True) # unsure what to name this field/what it is supposed to provide
	dba_name = models.CharField(max_length=256, null=True, blank=True)
	borrower_type = models.IntegerField(
		choices = BORROWER_CHOICES,
		default = 0,
	)
	title = models.CharField(max_length=256)
	authorized = models.BooleanField()
	ssn = models.IntegerField()
	tin_no = models.IntegerField(null=True, blank=True)
	home_phone = models.CharField(max_length=256)
	dob = models.DateField(default=timezone.now)
	yrs_school = models.IntegerField() # years of schooling completed
	marital_status = models.IntegerField(
		choices = MARITAL_CHOICES,
		default = 0,
	)
	dependents = models.IntegerField()
	present_addr = models.ForeignKey(Address, related_name='present_addr', null=True, blank=True)
	own_rent = models.IntegerField(
		choices = OWN_RENT_CHOICES,
		default = 0,
	)
	living_yrs = models.IntegerField() # years owned/rented at property referenced in present_addr
	mail_addr = models.CharField(max_length=256)
	principal_office_addr = models.CharField(max_length=256, null=True, blank=True)
	orginizations_state = models.IntegerField(
		choices = STATE_CHOICES,
		default = 0,
	)
	
	# below are fields to be filled out if own_rent < 2
	former_addr = models.ForeignKey(Address, related_name='former_addr', null=True, blank=True)
	former_own_rent = models.IntegerField(
		choices = OWN_RENT_CHOICES_NULL,
		default = 2,
	)
	former_lived_yrs = models.IntegerField(null=True, blank=True) # years owned/rented at property referenced \
													# in former_addr
								
	business = models.ForeignKey(BusinessInfo, null=True, blank=True)
	expenses = models.ForeignKey(ExpenseInfo, null=True, blank=True)
	assets_liabilities = models.ForeignKey(ALSummary, null=True, blank=True)
	declarations = models.ForeignKey(Declaration, null=True, blank=True)
	filing_dates = models.DateField(default=timezone.now)
	filing_locations = models.CharField(max_length=256, null=True, blank=True) # will probably want this to be a foreign key, possibly Address(?)
	
class AcknowledgeAgree(models.Model):
	borrower = models.ForeignKey(BorrowerInfo, related_name='borrower_agree', null=True, blank=True)
	borrower_agree = models.BooleanField(default=False)
	coborrower = models.ForeignKey(BorrowerInfo, related_name='coborrower_agree', null=True, blank=True)
	coborrower_agree = models.BooleanField(default=False)
	date = models.DateField(default=timezone.now)
	

class CreditRequest(models.Model):
	CREDIT_REQUEST_CHOICES = (
		(0, 'Applicant Only'),
		(1, 'Joint with Co-Applicant(s)'),
	)
	borrower = models.ForeignKey(BorrowerInfo, null=True, blank=True)
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
	submission_date = models.DateField(default=timezone.now)
	
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
	loan_officer = models.ForeignKey(User, limit_choices_to = {'user__is_staff__exact': True }, related_name='loan_officer')
	officer_number = models.IntegerField()
	approved_by = models.ForeignKey(User, limit_choices_to = {'user__is_staff__exact': True }, related_name='loan_approver')
	concurrence_by = models.ForeignKey(User, limit_choices_to = {'user__is_staff__exact': True }, related_name='loan_concurrer') # 'loan_concurrer' <- yikes
	committee_date = models.DateField()
	decision_date = models.DateField()
	branch = models.CharField(max_length=256) # this could be an Address (?)
	app_date = models.DateField()
	app_number = models.IntegerField()
	commitment_number = models.IntegerField()
	loan_number = models.IntegerField()
	mortgage_loan_originator_id = models.CharField(max_length=256)# may turn into FK with 'user__is_staff__exact':True
	mortgage_loan_company_id = models.CharField(max_length=256) # will probably turn into FK - unsure to what table though, may need to make a new one
	decision = models.IntegerField(
		choices = DECISION_CHOICES,
		default = 0,
	)
	
# model based on existing LoanWorkflow model, the other one has	\
# been commented out to prevent any kind of duplication error	
class LoanWorkflow(models.Model):
	credit_approval = models.BooleanField(default=False)
	credit_approval_timestamp = models.DateTimeField(default=timezone.now)
	data_merge = models.BooleanField(default=False)
	data_merge_officer = models.ForeignKey(User, limit_choices_to={'user__is_staff__exact':True})
	data_merge_timestamp = models.DateTimeField(default=timezone.now)
	agreement = models.BooleanField(default=False)
	borrower = models.ForeignKey(BorrowerInfo, related_name='w_borrower')
	coborrower = models.ForeignKey(BorrowerInfo, related_name='w_coborrower', null=True, blank=True)
	agreement_timestamp = models.DateTimeField(default=timezone.now)
	
# Below is a Loan Summary, all relevant information at a glance should be put here
class LoanSummary(models.Model):
	subject_address = models.ForeignKey(PropertyInfo)
	borrower = models.ForeignKey(BorrowerInfo, related_name='borrower')
	coborrower = models.ForeignKey(BorrowerInfo, related_name='coborrower', null=True, blank=True)
	lender_info = models.ForeignKey(LenderInfo)
	loan_terms = models.ForeignKey(LoanTerms)
	
	
	
# Will probably end up removing this model for now, as it is something that 
# can't be useful until like 3 years from now when TLC has repeat customers
# and want to track their own records based on each customer
'''# Totally unsure of what this model is going to provide
# or even where it goes/connects to
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
	last_credit_bureau = models.CharField(max_length=256, null=True, blank=True)
	
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
	proposed_total = models.DecimalField(max_digits=12, decimal_places=2)'''