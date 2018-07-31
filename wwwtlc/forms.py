from django import forms
from wwwtlc.add_new import SelectWithPop, MultipleSelectWithPop

# some of the following models may need to be removed
# will handle later
from wwwtlc.models_bse import (
AcknowledgeAgree, ApplicationSummary, AssetSummary,
BankAccount, BankAccount, BorrowerInfo, BusinessInfo,
ConstructionInfo, CreditRequest, Declaration, EmploymentIncome,
ManagedProperty, PropertyInfo
)

from wwwtlc.models_meta import (
Bank, Bank_Account, Borrower, Contract, Credit_Report,
Partner, Person, Verified, Wallet
)

from wwwtlc.models_officer import (
LenderInfo, LoanPaymentHistory, LoanSummary, 
LoanTerms, NewLoan
)

from wwwtlc.models_loan_apply import (
Address, ContactRequest, PropertyInfoRequest, CurrentMortgage,
MortgageDesired, BorrowerInfoRequest, NewRequestSummary
)
		
# Below are forms for the new models - correlates to models_loan_app.py

# models not listed in the forms, due to only needing to be accessed by staff:
#	- LenderInfo
#	- LoanWorkflow
#	- LoanSummary

class AcknowledgeAgreeForm(forms.ModelForm):
	step_name = 'Acknowledgement & Agreement:'
	class Meta:
		model = AcknowledgeAgree
		exclude = ['source']
		widgets = {
			'borrower' : SelectWithPop,
			'coborrower' : SelectWithPop,
		}
		
class AddressForm(forms.ModelForm):
	step_name = 'Property Address:'
	class Meta:
		model = Address
		exclude = ['user', 'source']
		
class AppStatusForm(forms.ModelForm):
	class Meta:
		model = ApplicationSummary
		fields = ['status']

class AppTierForm(forms.ModelForm):
	class Meta:
		model = ApplicationSummary
		fields = ['tier']

class AssetSummaryForm(forms.ModelForm):
	step_name = 'Asset Summary:'
	class Meta:
		model = AssetSummary
		fields = ['life_ins_value', 'stock_value', 'bond_value', 'face_amount', 'subtotal_liquid', 'vested_interest', 'net_worth', 'other_description', 'other_amt_total', 'assets_total']
		
class BankAccountForm(forms.ModelForm):
	step_name = 'Bank Account(s):'
	class Meta:
		model = BankAccount
		exclude = ['source']
		widgets = {
			'address' : SelectWithPop
		}	

class BorrowerInfoForm(forms.ModelForm):
	step_name = 'Borrower Information:'
	class Meta:
		model = BorrowerInfo
		exclude = ['user', 'source', 'business', 'assets_liabilities', 'declarations']
		widgets = {
			'present_addr' : SelectWithPop,
			'mail_addr' : SelectWithPop,
			'former_addr' : SelectWithPop,
			'principal_office_addr' : SelectWithPop
		}
		
	def __init__(self, *args, **kwargs):
		super(BorrowerInfoForm, self).__init__(*args, **kwargs)
		if 'initial' in kwargs:
			y = kwargs['initial'].values()
			user = next(iter(y))
			self.fields['present_addr'].queryset = Address.objects.filter(user=user).order_by('-id')
			self.fields['present_addr'].empty_label = None
			self.fields['mail_addr'].queryset = Address.objects.filter(user=user).order_by('-id')
			self.fields['mail_addr'].empty_label = None
			self.fields['former_addr'].queryset = Address.objects.filter(user=user).order_by('-id')
			self.fields['principal_office_addr'].queryset = Address.objects.filter(user=user).order_by('-id')
			
class BusinessInfoForm(forms.ModelForm):
	step_name = 'Business Information:'
	class Meta:
		model = BusinessInfo
		exclude = ['source']

class ConstructionInfoForm(forms.ModelForm):
	step_name = 'Construction Information (if applicable):'
	class Meta:
		model = ConstructionInfo
		exclude = ['source']
		
class CreditRequestForm(forms.ModelForm):
	step_name = 'Credit Request:'
	class Meta:
		model = CreditRequest
		exclude = ['source', 'borrower', 'application']
		
class DeclarationForm(forms.ModelForm):
	step_name = 'Declarations:'
	class Meta:
		model = Declaration
		exclude = ['source']

class EmploymentIncomeForm(forms.ModelForm):
	step_name = 'Employment Income Information:'
	class Meta:
		model = EmploymentIncome
		exclude = ['source']
		widgets = {
			'address' : SelectWithPop
		}		

class LoanForm(forms.ModelForm):
	step_name = 'Loan:'
	class Meta:
		model = NewLoan
		exclude = ['user', 'borrower', 'coborrower', 'loan_terms', 'loan_wallet']
		
class LoanTermsForm(forms.ModelForm):
	step_name = 'Loan Terms:'
	class Meta:
		model = LoanTerms
		exclude = ['application']

class ManagedPropertyForm(forms.ModelForm):
	step_name = 'Managed Properties:'
	class Meta:
		model = ManagedProperty
		exclude = ['source']
		widgets = {
			'property_address' : SelectWithPop
		}		
		
class PaymentForm(forms.ModelForm):
	class Meta:
		model = LoanPaymentHistory
		exclude = ['wallet', 'loan']

class PropertyInfoForm(forms.ModelForm):
	step_name = 'Property Information:'
	class Meta:
		model = PropertyInfo
		exclude = ['source', 'construction_loan', 'refinance_loan', 'legal_description']
		widgets = {
			'address' : SelectWithPop
		}
		
	# Only shows users Addresses assigned to them when filling out the form	
	def __init__(self, *args, **kwargs):
		y = kwargs['initial'].values()
		user = next(iter(y))
		super(PropertyInfoForm, self).__init__(*args, **kwargs)
		self.fields['address'].queryset = Address.objects.filter(user=user).order_by('-id')
		self.fields['address'].empty_label = None

class WalletForm(forms.ModelForm):
	step_name = 'Loan Wallet:'
	class Meta:
		model = Wallet
		exclude = ['wallet']
		
''' 
Below are super disgusting hack and slash forms for the new loanapply
form specified in the email recieved on 7/17
'''

class ContactRequestForm(forms.ModelForm):
	step_name = 'Contact:'
	class Meta:
		model = ContactRequest
		exclude = ['source']
		
class PropertyInfoRequestForm(forms.ModelForm):
	step_name = 'Property Information:'
	class Meta:
		model = PropertyInfoRequest
		exclude = ['source']
		widgets = {
			'property_address' : SelectWithPop
		}
		
	# Only shows users Addresses assigned to them when filling out the form	
	def __init__(self, *args, **kwargs):
		y = kwargs['initial'].values()
		user = next(iter(y))
		super(PropertyInfoRequestForm, self).__init__(*args, **kwargs)
		self.fields['property_address'].queryset = Address.objects.filter(user=user).order_by('-id')
		self.fields['property_address'].empty_label = None
		
class CurrentMortgageForm(forms.ModelForm):
	step_name = 'Current Mortgage:'
	class Meta:
		model = CurrentMortgage
		exclude = ['source']
		
class MortgageDesiredForm(forms.ModelForm):
	step_name = 'Mortgage Desired:'
	class Meta:
		model = MortgageDesired
		exclude = ['source']
		
class BorrowerInfoRequestForm(forms.ModelForm):
	step_name = 'Borrower Information:'
	class Meta:
		model = BorrowerInfoRequest 
		exclude = ['source', 'language']
		
# Form for 'Submit a Loan'
class BorrowerInfoLoanForm(forms.ModelForm):
	step_name = 'Loan Borrower Information:'
	class Meta:
		model = BorrowerInfo
		exclude = ['source', 'business', 'assets_liabilities', 'declarations']