import datetime
from decimal import Decimal

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

from wwwtlc.models_loan_apply import Address

# Models included in BOTH Basic and Standard applications
class BusinessInfo(models.Model):
	source = models.ForeignKey(User)
	bus_name = models.CharField(max_length=256, verbose_name='Business Name', help_text='(required)')
	bus_description = models.TextField(verbose_name='Business Description', help_text='(required)')
	income = models.DecimalField(max_digits=12, decimal_places=4, verbose_name='Income', help_text='(required)')
	rent = models.DecimalField(max_digits=12, decimal_places=4, null=True, blank=True)
	first_mortgage = models.DecimalField(max_digits=12, decimal_places=4, null=True, blank=True, verbose_name='First Mortgage Amount')
	other_mortgage_amt = models.DecimalField(max_digits=12, decimal_places=4, null=True, blank=True, verbose_name='Other Mortgage Amount')
	other_mortgage_description = models.TextField(null=True, blank=True, verbose_name='Other Mortgage Description')
	hazard_insur = models.DecimalField(max_digits=12, decimal_places=4, null=True, blank=True, verbose_name='Hazard Insurance')
	real_estate_taxes = models.DecimalField(max_digits=12, decimal_places=4, null=True, blank=True, verbose_name='Real Estate Taxes')
	net_rental = models.DecimalField(max_digits=12, decimal_places=4, null=True, blank=True, verbose_name='Net Rental Income')
	income_other_description = models.TextField(null=True, blank=True, verbose_name='Other Income')
	income_other = models.DecimalField(max_digits=12, decimal_places=4, null=True, blank=True, verbose_name='Other Income Total')
	income_total = models.DecimalField(max_digits=12, decimal_places=4, verbose_name='Income Total', help_text='(required)')
	expense_other_description = models.TextField(null=True, blank=True, verbose_name='Other Expense(s)')
	expense_other = models.DecimalField(max_digits=12, decimal_places=4, null=True, blank=True, verbose_name='Other Expense Total')
	expense_total = models.DecimalField(max_digits=12, decimal_places=4, verbose_name='Expense Total', help_text='(required)')
		
class ConstructionInfo(models.Model):
	source = models.ForeignKey(User)
	year_acquired = models.DateField(default=timezone.now, null=True, blank=True, verbose_name='Year Acquired')
	original_cost = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True, verbose_name='Original Cost')
	amt_existing_liens = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True, verbose_name='Existing Liens Amount')
	present_value = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True, verbose_name='Present Value', help_text='a.') # a.
	improve_cost = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True, verbose_name='Cost of Improvements', help_text='b.') # b.
	total = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True, help_text='a. + b.') # (a + b)
	
class PropertyInfo (models.Model):
	source = models.ForeignKey(User)
	address = models.ForeignKey(Address, null=True, blank=True)
	no_units = models.IntegerField(verbose_name='Number of Units', help_text='(required)') # number of units
	legal_description = models.CharField(max_length=256, null=True, blank=True, verbose_name='Legal Description')
	year_built = models.IntegerField(verbose_name='Year Built', help_text='(required)')
	construction_loan = models.ForeignKey(ConstructionInfo, null=True, blank=True, verbose_name='Construction Loan')
	title_names = models.CharField(max_length=256, null=True, blank=True, verbose_name='Names on Title')
	
class Declaration(models.Model):
	source = models.ForeignKey(User)
	# on pdf, it states: "If 'Yes' to any questions a-i, use continuation sheet for explanation"	\
	# I put a textbox in this model to satisfy this requirement
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
	
	explanation = models.TextField(null=True, blank=True, verbose_name='Explanation')
			
# Models Basic Only
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
	source = models.ForeignKey(User, related_name='borrower_info_source')	
	application_type = models.IntegerField(
		choices = APPLICATION_CHOICES,
		default = 0,
		verbose_name = 'Application Type'
	)
	name_first = models.CharField(max_length=256, verbose_name='First Name', help_text='(required)')
	name_middle = models.CharField(max_length=30, null=True, blank=True, verbose_name='Middle Name')
	name_last = models.CharField(max_length=256, verbose_name='Last Name', help_text='(required)')
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
	dob = models.DateField(default=timezone.now, verbose_name='Date of Birth')
	marital_status = models.IntegerField(
		choices = MARITAL_CHOICES,
		default = 0,
		verbose_name = 'Marital Status'
	)
	present_addr = models.ForeignKey(Address, related_name='present_addr', null=True, blank=True, verbose_name='Present Address')
	own_rent = models.IntegerField(
		choices = OWN_RENT_CHOICES,
		default = 0,
		verbose_name = 'Do you Own or Rent?'
	)
	living_yrs = models.IntegerField(verbose_name='Years at Present Address', help_text='(required)')
	mail_addr = models.ForeignKey(Address, related_name='mail_address', verbose_name='Mailing Address', help_text='(required)')
	principal_office_addr = models.ForeignKey(Address, related_name='principal_office_addres', null=True, blank=True, verbose_name='Principal Office Address')
	organizations_state = models.IntegerField(
		choices = STATE_CHOICES,
		default = 0,
		verbose_name = 'Organization\'s State'
	)
	
	# below are fields to be filled out if own_rent < 2
	former_addr = models.ForeignKey(Address, related_name='former_addr', null=True, blank=True, verbose_name='Former Address (if less than 2 years)')
	former_own_rent = models.IntegerField(
		choices = OWN_RENT_CHOICES_NULL,
		default = 2,
		verbose_name = 'Did you Own or Rent?'
	)
	former_lived_yrs = models.IntegerField(null=True, blank=True, verbose_name='Years at Former Address') # years owned/rented at property referenced \
													# in former_addr
								
	business = models.ForeignKey(BusinessInfo, null=True, blank=True)
	declarations = models.ForeignKey(Declaration, null=True, blank=True)
	
	def __str__(self):
		return self.name_last + ', ' + self.name_first
		
class AcknowledgeAgree(models.Model):
	source = models.ForeignKey(User)
	borrower = models.ForeignKey(BorrowerInfo, related_name='borrower_agree', null=True, blank=True)
	borrower_agree = models.BooleanField(default=False, verbose_name='Borrower\'s Acknowledgement')
	coborrower = models.ForeignKey(BorrowerInfo, related_name='coborrower_agree', null=True, blank=True, verbose_name='Co-Borrower')
	coborrower_agree = models.BooleanField(default=False, verbose_name='Co-Borrower\'s Acknowledgement')
	date = models.DateField(default=timezone.now)
			
class ApplicationSummary(models.Model):
	STATUS_CHOICES = (
		(0, 'New'),
		(1, 'Requires Additional User Information'),
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
		(13, 'Deed Published'),
		(14, 'Declared on Blockchain'),
	)
	TIER_CHOICES = (
		(0, 'Basic'),
		(1, 'Standard'),
		#(2, 'Extended'),
	)
	source = models.ForeignKey(User, related_name='application_summary_source')
	user = models.ForeignKey(User)
	application = models.ForeignKey('self', null=True, blank=True)
	property = models.ForeignKey(PropertyInfo)
	borrower = models.ForeignKey(BorrowerInfo, related_name='borrower')
	coborrower = models.ForeignKey(BorrowerInfo, related_name='coborrower', null=True, blank=True)
	acknowledge = models.ForeignKey(AcknowledgeAgree)
	status = models.IntegerField(
		choices = STATUS_CHOICES,
		default = 0,
	)
	tier = models.IntegerField(
		choices = TIER_CHOICES,
		default = 0,
	)
	submission_date = models.DateTimeField(default=timezone.now)
	resubmission_date = models.DateTimeField(null=True, blank=True)
	approval_date = models.DateTimeField(null=True, blank=True)
	certification_date = models.DateTimeField(null=True, blank=True)
	blockchain_declared_date = models.DateTimeField(null=True, blank=True)
		
class CreditRequest(models.Model):
	LOAN_TYPE_CHOICES = (
		(0, 'Fixed'),
		(1, 'ARM'),
	)
	PURPOSE_CHOICES = (
		(0, 'Rate and Term'),
		(1, 'Cash Out'),
	)
	source = models.ForeignKey(User)
	borrower = models.ForeignKey(BorrowerInfo, null=True, blank=True)
	amt_requested = models.DecimalField(max_digits=12, decimal_places=2, verbose_name='Amount Requested', help_text='(required)')
	term_requested = models.CharField(max_length=256, verbose_name='Term Requested', help_text='(required)') # unsure of what this is going to be
	loan_type = models.IntegerField(
		choices = LOAN_TYPE_CHOICES,
		default = 0,
	)
	request_purpose = models.IntegerField(
		choices = PURPOSE_CHOICES,
		default = 0,
	)
	application = models.ForeignKey(ApplicationSummary, null=True, blank=True)
	submission_date = models.DateField(default=timezone.now, verbose_name='Date of Submission')
	
# Models Standard Only
class EmploymentIncome(models.Model): # for Tier 2, when personal income is needed for the application
	source = models.ForeignKey(User)
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
		
class BankAccount(models.Model):
	source = models.ForeignKey(User)
	name = models.CharField(max_length=256, null=True, blank=True, verbose_name='Name of Bank, S&L, or Credit Union')
	address = models.ForeignKey(Address, null=True, blank=True)
	acct_no = models.IntegerField(null=True, blank=True, verbose_name='Account Number')
	amount = models.DecimalField(max_digits=12, decimal_places=4, null=True, blank=True, verbose_name='Cash or Market Value')
		
class AssetSummary(models.Model):
	source = models.ForeignKey(User)
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
	stock_value = models.DecimalField(decimal_places=4, max_digits=12, verbose_name='Stock Value')
	bond_value = models.DecimalField(decimal_places=4, max_digits=12, verbose_name='Bond Value')
	
	life_ins_value = models.DecimalField(max_digits=12, decimal_places=4, null=True, blank=True, verbose_name='Life Insurance Value')
	face_amount = models.DecimalField(max_digits=12, decimal_places=4, null=True, blank=True, verbose_name='Face Amount')
	subtotal_liquid = models.DecimalField(max_digits=12, decimal_places=4, verbose_name='Subtotal Liquid Assets', help_text='(required)')
	vested_interest = models.DecimalField(max_digits=12, decimal_places=4, null=True, blank=True, verbose_name='Vested Interest in Retirement Fund')
	net_worth = models.DecimalField(max_digits=12, decimal_places=4, null=True, blank=True, verbose_name='Net Worth of Business(es) Owned') # of business(es) owned
	
	employment_income = models.ForeignKey(EmploymentIncome, null=True, blank=True, verbose_name='Employment Income Information')
	
	other_description = models.TextField(null=True, blank=True, verbose_name='Other Assets', help_text='(itemize)')
	other_amt_total = models.DecimalField(max_digits=12, decimal_places=2, verbose_name='Other Assets Total', help_text='(required)')
	
	assets_total = models.DecimalField(max_digits=12, decimal_places=4, verbose_name='Assets Total', help_text='(required)')
		
class ManagedProperty(models.Model):
	source = models.ForeignKey(User)
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