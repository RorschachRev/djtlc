import datetime
from decimal import Decimal
from django.db import models
from django.utils import timezone
from .models import Address
from django.contrib.auth.models import User

#********************************************************************************************
# TODO'S:
#____________________________________________________________________________________________
#
#	- Read through all comments and handle each question/design concern
#	- Trim down any unecessary/redundant fields
#	- delete all commented code that can't fit into the new schema
#	
#********************************************************************************************
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
		verbose_name = 'Mortgage Type'
	)
	agency_case_no = models.IntegerField(verbose_name='Agency Case Number', help_text='(required)')
	lender_case_no = models.IntegerField(verbose_name='Lender Case Number', help_text='(required)')
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
		
# Added null=True & blank=True to both ConstructionInfo	\
# and RefinanceInfo models so that the form doesn't require 	\
# them. Will want to change this later on the next revision of	\
# the form. If CI || RI is_applicable, display forms, else don't	\
# kinda thing where the forms will require information if theyre displayed
class ConstructionInfo(models.Model):
	year_acquired = models.DateField(default=timezone.now, null=True, blank=True, verbose_name='Year Acquired')
	original_cost = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True, verbose_name='Original Cost')
	amt_existing_liens = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True, verbose_name='Existing Liens Amount')
	present_value = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True, verbose_name='Present Value', help_text='a.') # a.
	improve_cost = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True, verbose_name='Cost of Improvements', help_text='b.') # b.
	total = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True, help_text='a. + b.') # (a + b)
	
	def __str__(self):
		return str(self.total)
	
class RefinanceInfo(models.Model):
	year_acquired = models.DateField(default=timezone.now, null=True, blank=True, verbose_name='Year Acquired')
	original_cost = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True, verbose_name='Original Cost')
	amt_existing_liens = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True, verbose_name='Existing Liens Amount')
	refine_purpose = models.CharField(max_length=256, null=True, blank=True, verbose_name='Purpose of Refinance')
	total_cost = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True, verbose_name='Total')
	
	def __str__(self):
		return str(self.total_cost)
	
class PropertyInfo (models.Model):
	address = models.ForeignKey(Address, null=True, blank=True)
	no_units = models.IntegerField(verbose_name='Number of Units', help_text='(required)') # number of units
	legal_description = models.CharField(max_length=256, verbose_name='Legal Description', help_text='(required)')
	year_built = models.IntegerField(verbose_name='Year Built', help_text='(required)')
	construction_loan = models.ForeignKey(ConstructionInfo, null=True, blank=True, verbose_name='Construction Loan')
	refinance_loan = models.ForeignKey(RefinanceInfo, null=True, blank=True, verbose_name='Refinance Loan')
	title_names = models.CharField(max_length=256, null=True, blank=True, verbose_name='Names on Title') #will probably want a many-to-many relation - unsure if should be linked to BorrowerInfo or not
	
	def __str__(self):
		return str(self.address) + ', ' + self.legal_description
								      
class EmploymentIncome(models.Model): # for Tier 2, when personal income is needed for the application
	name = models.CharField(max_length=256, help_text='(required)', verbose_name='Name of Employer')
	address = models.ForeignKey(Address, null=True, blank=True)
	self_employed = models.BooleanField(default=False, verbose_name='Self Employed')
	yrs_worked = models.IntegerField(null=True, blank=True, verbose_name='Years Worked at Current Employer') # years worked at current employer
	yrs_in_profession = models.IntegerField(null=True, blank=True, verbose_name='Years Worked in Related Field') # years worked in the related field
	position = models.CharField(max_length=256, null=True, blank=True)
	title = models.CharField(max_length=256, help_text='(required)')
	business_type = models.CharField(max_length=256, null=True, blank=True, verbose_name='Type of Business')
	business_phone = models.CharField(max_length=256, null=True, blank=True, verbose_name='Phone Number')
	income = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True, verbose_name='Yearly Income') # yearly amt
	
	# if yrs_worked < 2 || if working in more than one position, 	\
	# the following fields will need to be created / filled out:		\
	other_emp_info = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, verbose_name='Other Employment Information', help_text='If employed for less than two years or if employed currently in more than one position') # recursive relationship
	
	def __str__(self):
		return '{}, {}: ${}'.format(self.name, self.title, self.income)
		
# I feel as though this model contains comprehensive expense information	\
# but insufficient income information, may need to add more 'income' fields
class BusinessInfo(models.Model):
	bus_name = models.CharField(max_length=256, verbose_name='Business Name', help_text='(required)')
	bus_description = models.TextField(verbose_name='Business Description', help_text='(required)')
	base_empl_income = models.DecimalField(max_digits=12, decimal_places=4, verbose_name='Base Employee Income', help_text='(required)')
	rent = models.DecimalField(max_digits=12, decimal_places=4, null=True, blank=True)
	first_mortgage = models.DecimalField(max_digits=12, decimal_places=4, null=True, blank=True, verbose_name='First Mortgage Amount')
	other_financing = models.DecimalField(max_digits=12, decimal_places=4, null=True, blank=True, verbose_name='Other Financing Amount')
	other_financing_description = models.TextField(null=True, blank=True, verbose_name='Other Financing Description')
	hazard_insur = models.DecimalField(max_digits=12, decimal_places=4, null=True, blank=True, verbose_name='Hazard Insurance')
	real_estate_taxes = models.DecimalField(max_digits=12, decimal_places=4, null=True, blank=True, verbose_name='Real Estate Taxes')
	mortgage_insur = models.DecimalField(max_digits=12, decimal_places=4, null=True, blank=True, verbose_name='Mortgage Insurance')
	overtime = models.DecimalField(max_digits=12, decimal_places=4, null=True, blank=True)
	bonuses = models.DecimalField(max_digits=12, decimal_places=4, null=True, blank=True)
	commissions = models.DecimalField(max_digits=12, decimal_places=4, null=True, blank=True)
	dividends = models.DecimalField(max_digits=12, decimal_places=4, null=True, blank=True)
	interest = models.DecimalField(max_digits=12, decimal_places=4, null=True, blank=True)
	net_rental = models.DecimalField(max_digits=12, decimal_places=4, null=True, blank=True, verbose_name='Net Rental Income')
	income_other_description = models.TextField(null=True, blank=True, verbose_name='Other Income')
	income_other = models.DecimalField(max_digits=12, decimal_places=4, null=True, blank=True, verbose_name='Other Income Total')
	income_total = models.DecimalField(max_digits=12, decimal_places=4, verbose_name='Income Total', help_text='(required)')
	expense_other_description = models.TextField(null=True, blank=True, verbose_name='Other Expense(s)')
	expense_other = models.DecimalField(max_digits=12, decimal_places=4, null=True, blank=True, verbose_name='Other Expense Total')
	expense_total = models.DecimalField(max_digits=12, decimal_places=4, verbose_name='Expense Total', help_text='(required)')
	net_revenue = models.DecimalField(max_digits=12, decimal_places=4, verbose_name='Net Revenue', help_text='(required)')
	
	def __str__(self):
		return self.bus_name + ', $' + str(self.net_revenue)
	
class BankAccount(models.Model):
	name = models.CharField(max_length=256, null=True, blank=True, verbose_name='Name of Bank, S&L, or Credit Union')
	address = models.CharField(max_length=256, null=True, blank=True)
	acct_no = models.IntegerField(null=True, blank=True, verbose_name='Account Number')
	amount = models.DecimalField(max_digits=12, decimal_places=4, null=True, blank=True, verbose_name='Cash or Market Value')
	
	def __str__(self):
		return str(self.acct_no) + ', $' + str(self.amount)
	
class Stock(models.Model):
	stock_name = models.CharField(max_length=256, null=True, blank=True, verbose_name='Company Name')
	stock_number = models.CharField(max_length=256, null=True, blank=True, verbose_name='Company Number')
	stock_description = models.TextField(null=True, blank=True, verbose_name='Stock Description')
	stock_amount = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True, verbose_name='Cash or Market Value')
	
	def __str__(self):
		return str(self.stock_number) + ', $' + str(self.stock_amount)
	
class Bond(models.Model):
	bond_name = models.CharField(max_length=256, null=True, blank=True, verbose_name='Company Name')
	bond_number = models.CharField(max_length=256, null=True, blank=True, verbose_name='Company Number')
	bond_description = models.TextField(null=True, blank=True, verbose_name='Bond Description')
	bond_amount = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True, verbose_name='Cash or Market Value')
	
	def __str__(self):
		return str(self.bond_number) + ', $' + str(self.bond_amount)
	
class Vehicle(models.Model):
	vehicle_make = models.CharField(max_length=256, null=True, blank=True, verbose_name='Make')
	vehicle_model = models.CharField(max_length=256, null=True, blank=True, verbose_name='Model')
	vehicle_amount = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True, verbose_name='Cash or Market Value')
	
	def __str__(self):
		return '{}, {} ${}'.format(self.vehicle_make, self.vehicle_model, self.vehicle_amount)
	
class AssetSummary(models.Model):
	holding_deposit = models.CharField(max_length=256, null=True, blank=True, verbose_name='Holding Deposit') # unsure what this field is supposed 	\
															       # to be. on pdf, it just states:			\
															       # "Cash deposit toward purchase		\
															       # held by:" and then a blank area to 	\
															       # fill out. Could be who is holding the	\
															       # deposit, or the deposit amount, I don't	\
															       # know
	# below fields are for listing checking & savings accounts
	acct1 = models.ForeignKey(BankAccount, related_name='acc_1', null=True, blank=True, verbose_name='Account 1')
	acct2 = models.ForeignKey(BankAccount, related_name='acc_2', null=True, blank=True, verbose_name='Account 2')
	acct3 = models.ForeignKey(BankAccount, related_name='acc_3', null=True, blank=True, verbose_name='Account 3')
	
	# below fields are for stocks
	stock1 = models.ForeignKey(Stock, related_name='stock_1', null=True, blank=True, verbose_name='Stock 1')
	stock2 = models.ForeignKey(Stock, related_name='stock_2', null=True, blank=True, verbose_name='Stock 2')
	stock3 = models.ForeignKey(Stock, related_name='stock_3', null=True, blank=True, verbose_name='Stock 3')
	stock4 = models.ForeignKey(Stock, related_name='stock_4', null=True, blank=True, verbose_name='Stock 4')
	stock5 = models.ForeignKey(Stock, related_name='stock_5', null=True, blank=True, verbose_name='Stock 5')
	
	# below fields are for bonds
	bond1 = models.ForeignKey(Bond, related_name='bond_1', null=True, blank=True, verbose_name='Bond 1')
	bond2 = models.ForeignKey(Bond, related_name='bond_2', null=True, blank=True, verbose_name='Bond 2')
	bond3 = models.ForeignKey(Bond, related_name='bond_3', null=True, blank=True, verbose_name='Bond 3')
	bond4 = models.ForeignKey(Bond, related_name='bond_4', null=True, blank=True, verbose_name='Bond 4')
	bond5 = models.ForeignKey(Bond, related_name='bond_5', null=True, blank=True, verbose_name='Bond 5')
	
	life_insur_net = models.DecimalField(max_digits=12, decimal_places=4, null=True, blank=True, verbose_name='Life Insurance Net Cash Value')
	face_amount = models.DecimalField(max_digits=12, decimal_places=4, null=True, blank=True, verbose_name='Face Amount')
	subtotal_liquid = models.DecimalField(max_digits=12, decimal_places=4, verbose_name='Subtotal Liquid Assets', help_text='(required)')
	vested_interest = models.DecimalField(max_digits=12, decimal_places=4, null=True, blank=True, verbose_name='Vested Interest in Retirement Fund')
	net_worth = models.DecimalField(max_digits=12, decimal_places=4, null=True, blank=True, verbose_name='Net Worth of Business(es) Owned') # of business(es) owned
	
	vehicle1 = models.ForeignKey(Vehicle, related_name='vehicle_1', null=True, blank=True, verbose_name='Vehicle 1')
	vehicle2 = models.ForeignKey(Vehicle, related_name='vehicle_2', null=True, blank=True, verbose_name='Vehicle 2')
	vehicle3 = models.ForeignKey(Vehicle, related_name='vehicle_3', null=True, blank=True, verbose_name='Vehicle 3')
	vehicle4 = models.ForeignKey(Vehicle, related_name='vehicle_4', null=True, blank=True, verbose_name='Vehicle 4')
	vehicle5 = models.ForeignKey(Vehicle, related_name='vehicle_5', null=True, blank=True, verbose_name='Vehicle 5')
	
	employment_income = models.ForeignKey(EmploymentIncome, null=True, blank=True, verbose_name='Employment Income Information')
	
	other_description = models.TextField(null=True, blank=True, verbose_name='Other Assets', help_text='(itemize)')
	other_amt_total = models.DecimalField(max_digits=12, decimal_places=2, verbose_name='Other Assets Total', help_text='(required)')
	
	assets_total = models.DecimalField(max_digits=12, decimal_places=4, verbose_name='Assets Total', help_text='(required)')
	
	def __str__(self):
		return str(self.assets_total)
	
class Debt(models.Model):
	company_name = models.CharField(max_length=256, null=True, blank=True, verbose_name='Company Name')
	company_address = models.CharField(max_length=256, null=True, blank=True, verbose_name='Company Address')
	acct_no = models.IntegerField(null=True, blank=True, verbose_name='Account Number')
	monthly_payment = models.DecimalField(max_digits=12, decimal_places=4, null=True, blank=True, verbose_name='Monthly Payment')
	months_left = models.IntegerField(null=True, blank=True, verbose_name='Months Left to Pay') # months left on monthly_payment
	unpaid_balance = models.DecimalField(max_digits=12, decimal_places=4, null=True, blank=True, verbose_name='Unpaid Balance')
	
	def __str__(self):
		return str(self.acct_no) + ', $' + str(self.unpaid_balance)
	
class Alimony(models.Model):
	owed_to = models.CharField(max_length=256, null=True, blank=True, verbose_name='Payments Owed to')
	amt_owed = models.DecimalField(max_digits=12, decimal_places=4, null=True, blank=True, verbose_name='Amount Owed')
	
	def __str__(self):
		return '$' + str(self.amt_owed) + '/month' 
	
class ChildSupport(models.Model):
	owed_to = models.CharField(max_length=256, null=True, blank=True, verbose_name='Payments Owed to')
	amt_owed = models.DecimalField(max_digits=12, decimal_places=4, null=True, blank=True, verbose_name='Amount Owed')
	
	def __str__(self):
		return '$' + str(self.amt_owed) + '/month' 
	
class SeparateMaint(models.Model):
	owed_to = models.CharField(max_length=256, null=True, blank=True, verbose_name='Payments Owed to')
	amt_owed = models.DecimalField(max_digits=12, decimal_places=4, null=True, blank=True, verbose_name='Amount Owed')
	
	def __str__(self):
		return '$' + str(self.amt_owed) + '/month' 
	
# previously in Liability summary block, unsure if this should go into the liability summary or the asset summary as a FK
class ManagedProperty(models.Model):
	real_estate_schedule = models.CharField(max_length=256, null=True, blank=True, verbose_name='Schedule of Real Estate') # may want to be a CHOICES field
	property_address = models.ForeignKey(Address, null=True, blank=True, verbose_name='Address of Property')
	property_type = models.CharField(max_length=256, null=True, blank=True, verbose_name='Type of Property') # will want to be CHOICES field
	present_market_value = models.DecimalField(max_digits=12, decimal_places=4, null=True, blank=True, verbose_name='Present Market Value')
	mortgage_amt = models.DecimalField(max_digits=12, decimal_places=4, null=True, blank=True, verbose_name='Mortgage Amount')
	liens_amt = models.DecimalField(max_digits=12, decimal_places=4, null=True, blank=True, verbose_name='Liens Amount')
	gross_rental_income = models.DecimalField(max_digits=12, decimal_places=4, null=True, blank=True, verbose_name='Gross Rental Income') # might want to require this
	mortgage_payments = models.DecimalField(max_digits=12, decimal_places=4, null=True, blank=True, verbose_name='Mortgage Payments')
	misc_payments = models.DecimalField(max_digits=12, decimal_places=4, null=True, blank=True, verbose_name='Miscellaneous Payments', help_text='(Insurance, Maintenance, Taxes, etc.)') # might want to require this
	net_rental_income = models.DecimalField(max_digits=12, decimal_places=4, null=True, blank=True, verbose_name='Net Rental Income') # might want to require this
	
	def __str__(self):
		return str(self.property_address) + ', $' + str(self.net_rental_income)
	
class LiabilitySummary(models.Model):
	debt1 = models.ForeignKey(Debt, related_name='debt1', null=True, blank=True, verbose_name='Debt 1')
	debt2 = models.ForeignKey(Debt, related_name='debt2', null=True, blank=True, verbose_name='Debt 2')
	debt3 = models.ForeignKey(Debt, related_name='debt3', null=True, blank=True, verbose_name='Debt 3')
	debt4 = models.ForeignKey(Debt, related_name='debt4', null=True, blank=True, verbose_name='Debt 4')
	debt5 = models.ForeignKey(Debt, related_name='debt5', null=True, blank=True, verbose_name='Debt 5')
	debt6 = models.ForeignKey(Debt, related_name='debt6', null=True, blank=True, verbose_name='Debt 6')
	
	alimony1 = models.ForeignKey(Alimony, related_name='alimony1', null=True, blank=True, verbose_name='Alimony 1')
	alimony2 = models.ForeignKey(Alimony, related_name='alimony2', null=True, blank=True, verbose_name='Alimony 2')
	alimony3 = models.ForeignKey(Alimony, related_name='alimony3', null=True, blank=True, verbose_name='Alimony 3')
	
	child_supp1 = models.ForeignKey(ChildSupport, related_name='child_supp1', null=True, blank=True, verbose_name='Child Support 1')
	child_supp2 = models.ForeignKey(ChildSupport, related_name='child_supp2', null=True, blank=True, verbose_name='Child Support 2')
	child_supp3 = models.ForeignKey(ChildSupport, related_name='child_supp3', null=True, blank=True, verbose_name='Child Support 3')
	
	separate_maint1 = models.ForeignKey(SeparateMaint, related_name='sep_maint1', null=True, blank=True, verbose_name='Separate Maintenance 1')
	separate_maint2 = models.ForeignKey(SeparateMaint, related_name='sep_maint2', null=True, blank=True, verbose_name='Separate Maintenance 2')
	separate_maint3 = models.ForeignKey(SeparateMaint, related_name='sep_maint3', null=True, blank=True, verbose_name='Separate Maintenance 3')
	
	job_related_expenses = models.DecimalField(max_digits=12, decimal_places=4, null=True, blank=True, verbose_name='Job Related Expenses')
	
	total_monthly_payments = models.DecimalField(max_digits=12, decimal_places=4, verbose_name='Total Monthly Payments', help_text='(required)')
	liabilities_total = models.DecimalField(max_digits=12, decimal_places=4, verbose_name='Total Liabilities', help_text='(required)')	
	
	def __str__(self):
		return str(self.liabilities_total)
	
class ALSummary(models.Model):
	joint = models.BooleanField(default=False, verbose_name='Joint Filing', help_text='Check if you are filing jointly') # Are you filing jointly or not?
	assets = models.ForeignKey(AssetSummary, null=True, blank=True, verbose_name='Assets Summary')
	liabilities = models.ForeignKey(LiabilitySummary, null=True, blank=True, verbose_name='Liabilities Summary')
	net_worth = models.DecimalField(max_digits=12, decimal_places=4, null=True, blank=True, verbose_name='Net Worth', help_text='(Assets - Liabilities)')
	annual_income = models.DecimalField(max_digits=12, decimal_places=2, verbose_name='Annual Income', help_text='(required)')
	annual_expenses = models.DecimalField(max_digits=12, decimal_places=2, verbose_name='Annual Expenses', help_text='(required)')
	net_annual_cash_flow = models.DecimalField(max_digits=12, decimal_places=2, verbose_name='Net Annual Cash Flow', help_text='(required)')
	
	# below fields are for listing any additional names under which credit has previously been recieved
	prev_alt_name = models.CharField(max_length=256, null=True, blank=True, verbose_name='Alternate Name')
	prev_creditor_name = models.CharField(max_length=256, null=True, blank=True, verbose_name='Creditor Name')
	prev_acct_no = models.IntegerField(null=True, blank=True, verbose_name='Account Number')
	
	def __str__(self):
		return 'Net Worth: ' + str(self.net_worth) + ' | Annual Cash Flow: ' + str(self.net_annual_cash_flow)
	
#***********************************************************************************************
# "Details of Transaction" -> SECTION VII/commercial_loan_app2.pdf					\
# will go here, but it will require some modification by Ian, is also part of officer workflow	\
# A lot of these fields have long names, I just briefly ran through it, so I didn't think of		\
# any good names to condense the field titles a bit more than they are					\
#***********************************************************************************************
class TransactionDetails(models.Model):
	purchase_price = models.DecimalField(max_digits=12, decimal_places=2, help_text='(required)') # a.
	alterations = models.DecimalField(max_digits=12, decimal_places=2, help_text='(required)') # b. 1/3
	improvements = models.DecimalField(max_digits=12, decimal_places=2, help_text='(required)') # b. 2/3
	repairs = models.DecimalField(max_digits=12, decimal_places=2, help_text='(required)') # b. 3/3
	land = models.DecimalField(max_digits=12, decimal_places=2, help_text='(required)') # c. # if acquired seperately
	refinance = models.DecimalField(max_digits=12, decimal_places=2, help_text='(required)') # d. # including debts to be paid off
	estimated_prepaid_items = models.DecimalField(max_digits=12, decimal_places=2, help_text='(required)') # e.
	estimated_closing_costs = models.DecimalField(max_digits=12, decimal_places=2, help_text='(required)') # f.
	pmi = models.DecimalField(max_digits=12, decimal_places=2, help_text='(required)') # g. 1/3
	mip = models.DecimalField(max_digits=12, decimal_places=2, help_text='(required)') # g. 2/3
	funding_fee = models.DecimalField(max_digits=12, decimal_places=2, help_text='(required)') # g. 3/3
	discount = models.DecimalField(max_digits=12, decimal_places=2, help_text='(required)') # h.
	total_costs = models.DecimalField(max_digits=12, decimal_places=2, help_text='(required)') # i. # add items a through h
	subordinate_financing = models.DecimalField(max_digits=12, decimal_places=2, help_text='(required)') # j.
	closing_cost_paid = models.DecimalField(max_digits=12, decimal_places=2, help_text='(required)') # k. # "Borrower's closing costs paid by Seller"
	other_credits_description = models.TextField(null=True, blank=True) # l. 1/2
	other_credits_total = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True) # l. 2/2
	loan_amount_exclude = models.DecimalField(max_digits=12, decimal_places=2, help_text='(required)') # m. # exclude PMI, MIP, Funding Fee financed
	financed_pmi = models.DecimalField(max_digits=12, decimal_places=2, help_text='(required)') # n. 1/3
	financed_mip = models.DecimalField(max_digits=12, decimal_places=2, help_text='(required)') # n. 2/3
	financed_funding_fee = models.DecimalField(max_digits=12, decimal_places=2, help_text='(required)') # n. 3/3
	loan_amount = models.DecimalField(max_digits=12, decimal_places=2, help_text='(required)') # o. # add m. & n.
	borrower_cash = models.DecimalField(max_digits=12, decimal_places=2, help_text='(required)') # p. # "Cash from/to Borrower (subtract j, k, l & o from i)
	
	def __str__(self):
		return 'Cash from/to Borrower: $' + str(self.borrower_cash)

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
	
	outstanding_judgements = models.BooleanField(default=False, verbose_name='Are there any outstanding judgements against you?', help_text='a.') # a.
	bankrupt = models.BooleanField(default=False, verbose_name='Have you been declared bankrupt within the past 7 years?', help_text='b.') # b.
	forclosed = models.BooleanField(default=False, verbose_name='Have you had property foreclosed upon or given title or deed in lieu thereof in the last 7 years?', help_text='c.') # c.
	lawsuit = models.BooleanField(default=False, verbose_name='Are you a party to a lawsuit?', help_text='d.') # d.
	obligated_forclosure = models.BooleanField(default=False, verbose_name='Have you directly or indirectly been obligated on any loan which resulted in foreclosure, transfer of title in lieu of foreclosure, or judgement?', help_text='e.') # e.
	delinquent_indefault = models.BooleanField(default=False, verbose_name='Are you presently delinquent or in default on any Federal debt or any other loan, mortgage, financial obligation, bond, or loan guarantee?', help_text='f.') # f.
	alimony = models.BooleanField(default=False, verbose_name='Are you obligated to pay alimony?', help_text='g. 1/3') # g. 1/3
	child_support = models.BooleanField(default=False, verbose_name='Are you obligated to pay child support?', help_text='g. 2/3') # g. 2/3
	seperate_maintenance = models.BooleanField(default=False, verbose_name='Are you obligated to pay separate maintenance?', help_text='g. 3/3') # g. 3/3
	borrowed_down_payment = models.BooleanField(default=False, verbose_name='Is any part of the down payment borrowed?', help_text='h.') # h.
	co_maker_endorser = models.BooleanField(default=False, verbose_name='Are you a co-maker or endorser on a note?', help_text='i.') # i.
	
	us_citizen = models.BooleanField(default=False, verbose_name='Are you a U.S. citizen?', help_text='j.') # j.
	permanent_res_alien = models.BooleanField(default=False, verbose_name='Are you a permanent resident alien?', help_text='k.') # k.
	primary_residence = models.BooleanField(default=False, verbose_name='Do you intend to occupy the property as your primary residence?', help_text='l. (If "Yes", complete question m below)') # l.
	
	# ownership_interest in the last 3 years		\
	# if True, user will need to fill out below fields
	
	ownership_interest = models.BooleanField(default=False, verbose_name='Have you had an ownership interest in a property in the last three years?', help_text='m. 1/3') # m. 1/3
	
	m_property_type = models.IntegerField(
		choices = PROPERTY_TYPE_CHOICES,
		default = 0,
		verbose_name = 'Property Type',
		help_text = 'm. 2/3',
	)# m. 2/3 # on pdf, it says "What type of property did	\
			# you own--principal residence (PR), second	\
			# home (SH), or investment property (IP)?	\
			# will probably just specify this in help_text later
			
	m_title_method = models.IntegerField(
		choices = TITLE_METHOD_CHOICES,
		default = 0,
		verbose_name = 'Title Method',
		help_text = 'm. 3/3',
	)# m 3/3 # there should be a better name for this field	\
			# on pdf, it says, "How did you hold title to 	\
			# the home -- solely by yourself (S), jointly 	\
			#with your spouse (SP), or jointly with 		\
			# another person (O)?"					\
			# will probably just specify this in help_text later
	
	continuation = models.TextField(null=True, blank=True, verbose_name='Continuation')
			
	def __str__(self):
		return 'Borrower\'s Declarations'
	
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
	user = models.ForeignKey(User)	
	application_type = models.IntegerField(
		choices = APPLICATION_CHOICES,
		default = 0,
		verbose_name = 'Application Type'
	)
	borrower_fname = models.CharField(max_length=256, verbose_name='First Name', help_text='(required)')
	borrower_lname = models.CharField(max_length=256, verbose_name='Last Name', help_text='(required)')
	applicant_type = models.IntegerField(
		choices = APPLICANT_CHOICES,
		default = 0,
		verbose_name = 'Applicant Type'
	)
	filing_type = models.IntegerField(
		choices = FILING_CHOICES,
		default = 0,
		verbose_name = 'Filing Type'
	)
	assumed_business_names = models.CharField(max_length=256, null=True, blank=True, verbose_name='Assumed Business Name(s)') # unsure what to name this field/what it is supposed to provide
	dba_name = models.CharField(max_length=256, null=True, blank=True, verbose_name='DBA Name')
	borrower_type = models.IntegerField(
		choices = BORROWER_CHOICES,
		default = 0,
		verbose_name = 'Borrower Type'
	)
	title = models.CharField(max_length=256, help_text='(required)')
	authorized = models.BooleanField()
	ssn = models.IntegerField(verbose_name='Social Security Number', help_text='(required)')
	tin_no = models.IntegerField(verbose_name='TIN Number', null=True, blank=True)
	home_phone = models.CharField(max_length=256, verbose_name='Home Phone', help_text='(required)')
	dob = models.DateField(default=timezone.now, verbose_name='Date of Birth')
	yrs_school = models.IntegerField(verbose_name='Years of Schooling Completed', help_text='(required)') # years of schooling completed
	marital_status = models.IntegerField(
		choices = MARITAL_CHOICES,
		default = 0,
		verbose_name = 'Marital Status'
	)
	dependents = models.IntegerField(help_text='(required)')
	present_addr = models.ForeignKey(Address, related_name='present_addr', null=True, blank=True, verbose_name='Present Address')
	own_rent = models.IntegerField(
		choices = OWN_RENT_CHOICES,
		default = 0,
		verbose_name = 'Do you Own or Rent?'
	)
	living_yrs = models.IntegerField(verbose_name='Years Owned/Rented at Present Address', help_text='(required)') # years owned/rented at property referenced in present_addr
	mail_addr = models.CharField(max_length=256, verbose_name='Mailing Address', help_text='(required)')
	principal_office_addr = models.CharField(max_length=256, null=True, blank=True, verbose_name='Pricipal Office Address')
	organizations_state = models.IntegerField(
		choices = STATE_CHOICES,
		default = 0,
		verbose_name = 'Organization\'s State'
	)
	
	# below are fields to be filled out if own_rent < 2
	former_addr = models.ForeignKey(Address, related_name='former_addr', null=True, blank=True, verbose_name='Former Address')
	former_own_rent = models.IntegerField(
		choices = OWN_RENT_CHOICES_NULL,
		default = 2,
		verbose_name = 'Did you Own or Rent?'
	)
	former_lived_yrs = models.IntegerField(null=True, blank=True, verbose_name='Years Owned/Rented at Former Address') # years owned/rented at property referenced \
													# in former_addr
								
	business = models.ForeignKey(BusinessInfo, null=True, blank=True)
	#expenses = models.ForeignKey(ExpenseInfo, null=True, blank=True)
	assets_liabilities = models.ForeignKey(ALSummary, null=True, blank=True, verbose_name='Assets & Liabilities Summary')
	declarations = models.ForeignKey(Declaration, null=True, blank=True)
	filing_dates = models.DateField(default=timezone.now, verbose_name='Filing Dates')
	filing_locations = models.CharField(max_length=256, null=True, blank=True, verbose_name='Filing Locations') # will probably want this to be a foreign key, possibly Address(?)
	
	def __str__(self):
		return self.borrower_lname + ', ' + self.borrower_fname + ': ' + str(self.business)
	
class AcknowledgeAgree(models.Model):
	borrower = models.ForeignKey(BorrowerInfo, related_name='borrower_agree', null=True, blank=True)
	borrower_agree = models.BooleanField(default=False, verbose_name='Borrower\'s Acknowledgement')
	coborrower = models.ForeignKey(BorrowerInfo, related_name='coborrower_agree', null=True, blank=True, verbose_name='Co-Borrower')
	coborrower_agree = models.BooleanField(default=False, verbose_name='Co-Borrower\'s Acknowledgement')
	date = models.DateField(default=timezone.now)
	
	def __str__(self):
		if self.coborrower != None and self.coborrower != '':
			return 'Borrower: ' + str(self.borrower) + ' | Co-Borrower: ' + str(self.coborrower)
		else:
			return 'Borrower: ' + str(self.borrower)

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
	
class ApplicationSummary(models.Model):
	STATUS_CHOICES = (
		(0, 'New'),
		(1, 'Requires Additional Information'),
		(2, 'Awaiting External Response'),
		(3, 'Resubmitted'),
		(4, 'Denied'),
		(5, 'Approved, Awaiting Certification'),
		(6, 'Escrow Filed'),
		(7, 'Escrow Completed'),
		(8, 'Title Filed'),
		(9, 'Title Completed'),
		(10, 'County Filed'),
		(11, 'County Completed'),
		(12, 'Certified'),
		(13, 'IPFS Published'),
		(14, 'Declared on Blockchain'),
	)
	user = models.ForeignKey(User)
	property = models.ForeignKey(PropertyInfo)
	borrower = models.ForeignKey(BorrowerInfo, related_name='borrower')
	coborrower = models.ForeignKey(BorrowerInfo, related_name='coborrower', null=True, blank=True)
	acknowledge = models.ForeignKey(AcknowledgeAgree)
	status = models.IntegerField(
		choices = STATUS_CHOICES,
		default = 0,
	)
	is_tier1 = models.BooleanField(default=False)
	is_tier2 = models.BooleanField(default=False)
	submission_date = models.DateTimeField(default=timezone.now)
	resubmission_date = models.DateTimeField(null=True, blank=True)
	approval_date = models.DateTimeField(null=True, blank=True)
	certification_date = models.DateTimeField(null=True, blank=True)
	blockchain_declared_date = models.DateTimeField(null=True, blank=True)
	
	def __str__(self):
		return str(self.id) + ', submitted: ' + str(self.submission_date)
	
# Below is a Loan Summary, all relevant information at a glance should be put here
class LoanSummary(models.Model):
	application = models.ForeignKey(ApplicationSummary, verbose_name='Application Summary')
	lender_info = models.ForeignKey(LenderInfo, verbose_name='Lender Information')
	loan_terms = models.ForeignKey(LoanTerms, verbose_name='Loan Terms')
	
	def __str__(self):
		return str(self.loan_terms)
		
class CreditRequest(models.Model):
	CREDIT_REQUEST_CHOICES = (
		(0, 'Applicant Only'),
		(1, 'Joint with Co-Applicant(s)'),
	)
	borrower = models.ForeignKey(BorrowerInfo, null=True, blank=True)
	amt_requested = models.DecimalField(max_digits=12, decimal_places=2, verbose_name='Amount Requested', help_text='(required)')
	term_requested = models.CharField(max_length=256, verbose_name='Term Requested', help_text='(required)') # unsure of what this is going to be
	loan_type = models.CharField(max_length=256, verbose_name='Loan Type', help_text='(required)') # will probably turn into a CHOICES field later
	market_survey = models.CharField(max_length=256, null=True, blank=True, verbose_name='Market Survey') # unsure of what this is going to be
	request_purpose = models.TextField(null=True, blank=True, verbose_name='Purpose of Request')
	application = models.ForeignKey(ApplicationSummary, null=True, blank=True)
	credit_request = models.IntegerField(
		choices = CREDIT_REQUEST_CHOICES,
		default = 0,
		verbose_name = 'Credit Request'
	)
	submission_date = models.DateField(default=timezone.now, verbose_name='Date of Submission')
	
	def __str__(self):
		return str(self.borrower) + ', $' + str(self.amt_requested) + ', ' + str(self.submission_date)
	
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
	
		
# commented out b/c I merged it into BusinessInfo, they contained a lot of redundant information	
'''class ExpenseInfo(models.Model):
	rent = models.DecimalField(max_digits=12, decimal_places=4, null=True, blank=True)
	first_mortgage = models.DecimalField(max_digits=12, decimal_places=4, null=True, blank=True)
	other_financing = models.DecimalField(max_digits=12, decimal_places=4, null=True, blank=True)
	hazard_insur = models.DecimalField(max_digits=12, decimal_places=4, null=True, blank=True)
	real_estate_taxes = models.DecimalField(max_digits=12, decimal_places=4, null=True, blank=True)
	mortgage_insur = models.DecimalField(max_digits=12, decimal_places=4, null=True, blank=True)
	base_empl_income = models.DecimalField(max_digits=12, decimal_places=4, help_text='(required)')
	overtime = models.DecimalField(max_digits=12, decimal_places=4, null=True, blank=True)
	bonuses = models.DecimalField(max_digits=12, decimal_places=4, null=True, blank=True)
	commissions = models.DecimalField(max_digits=12, decimal_places=4, null=True, blank=True)
	other_description = models.TextField(null=True, blank=True)
	expense_other = models.DecimalField(max_digits=12, decimal_places=4, null=True, blank=True)
	expense_total = models.DecimalField(max_digits=12, decimal_places=4, help_text='(required)')'''