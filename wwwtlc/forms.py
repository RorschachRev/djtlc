from django import forms
from wwwtlc.models import *
from wwwtlc.models_loan_app import *
		
# Below are forms for the new models - correlates to models_loan_app.py

# models not listed in the forms, due to only needing to be accessed by staff:
#	- LenderInfo
#	- Loan Terms
#	- LoanWorkflow
#	- LoanSummary

class AcknowledgeAgreeForm(forms.ModelForm):
	step_name = 'Acknowledgement & Agreement:'
	class Meta:
		model = AcknowledgeAgree
		fields = '__all__'
		
class AddressForm(forms.ModelForm):
	step_name = 'Property Address:'
	class Meta:
		model = Address
		fields = '__all__'
		
class AlimonyForm(forms.ModelForm):
	step_name = 'Alimony:'
	class Meta:
		model = Alimony
		fields = '__all__'

class ALSummaryForm(forms.ModelForm):
	step_name = 'Asset & Liability Information:'
	class Meta:
		model = ALSummary
		exclude = ['assets', 'liabilities']
		
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
		fields = ['life_insur_net', 'face_amount', 'subtotal_liquid', 'vested_interest', 'net_worth', 'other_description', 'other_amt_total', 'assets_total']
		
class BankAccountForm(forms.ModelForm):
	step_name = 'Bank Account(s):'
	class Meta:
		model = BankAccount
		fields = '__all__'
		
class BondForm(forms.ModelForm):
	step_name = 'Bond(s):'
	class Meta:
		model = Bond
		fields = '__all__'

class BorrowerInfoForm(forms.ModelForm):
	step_name = 'Borrower Information:'
	class Meta:
		model = BorrowerInfo
		exclude = ['user', 'business', 'assets_liabilities', 'declarations']
		
class BusinessInfoForm(forms.ModelForm):
	step_name = 'Business Information:'
	class Meta:
		model = BusinessInfo
		fields = '__all__'	

class ChildSupportForm(forms.ModelForm):
	step_name = 'Child Support:'
	class Meta:
		model = ChildSupport
		fields = '__all__'

class ConstructionInfoForm(forms.ModelForm):
	step_name = 'Construction Information (if applicable):'
	class Meta:
		model = ConstructionInfo
		fields = '__all__'
		
class CreditRequestForm(forms.ModelForm):
	step_name = 'Credit Request:'
	class Meta:
		model = CreditRequest
		exclude = ['borrower', 'application']

class DebtForm(forms.ModelForm):
	step_name = 'Debt(s):'
	class Meta:
		model = Debt
		fields = '__all__'
		
class DeclarationForm(forms.ModelForm):
	step_name = 'Declarations:'
	class Meta:
		model = Declaration
		fields = '__all__'	

class EmploymentIncomeForm(forms.ModelForm):
	step_name = 'Employment Income Information:'
	class Meta:
		model = EmploymentIncome
		fields = '__all__'	
		
class LiabilitySummaryForm(forms.ModelForm):
	step_name = 'Liability Summary:'
	class Meta:
		model = LiabilitySummary
		fields = ['job_related_expenses', 'total_monthly_payments', 'liabilities_total']

class ManagedPropertyForm(forms.ModelForm):
	step_name = 'Managed Properties:'
	class Meta:
		model = ManagedProperty
		fields = '__all__'
		
class PaymentForm(forms.ModelForm):
	class Meta:
		model = LoanPaymentHistory
		fields = '__all__'

class PropertyInfoForm(forms.ModelForm):
	step_name = 'Property Information:'
	class Meta:
		model = PropertyInfo
		exclude = ['address', 'construction_loan', 'refinance_loan']
		
class RefinanceInfoForm(forms.ModelForm):
	step_name = 'Refinance Information (if applicable):'
	class Meta:
		model = RefinanceInfo
		fields = '__all__'

class SeparateMaintForm(forms.ModelForm):
	step_name = 'Separate Maintenance:'
	class Meta:
		model = SeparateMaint
		fields = '__all__'
		
class StockForm(forms.ModelForm):
	step_name = 'Stock(s):'
	class Meta:
		model = Stock
		fields = '__all__'
		
class TransactionDetailsForm(forms.ModelForm):
	step_name = 'Transaction Details:'
	class Meta:
		model = TransactionDetails
		fields = '__all__'
		
class VehicleForm(forms.ModelForm):
	step_name = 'Vehicle(s):'
	class Meta:
		model = Vehicle
		fields = '__all__'

class WalletForm(forms.ModelForm):
	class Meta:
		model = Wallet
		fields = ['address']	
		
''' 
Below are super disgusting hack and slash forms for the new loanapply
form specified in the email recieved on 7/17
'''

class ContactRequestForm(forms.ModelForm):
	class Meta:
		model = ContactRequest
		fields = '__all__'
		
class PropertyInfoRequestForm(forms.ModelForm):
	class Meta:
		model = PropertyInfoRequest
		fields = '__all__'
		
class CurrentMortgageForm(forms.ModelForm):
	class Meta:
		model = CurrentMortgage
		fields = '__all__'
		
class MortgageDesiredForm(forms.ModelForm):
	class Meta:
		model = MortgageDesired
		fields = '__all__'
		
class BorrowerInfoRequestForm(forms.ModelForm):
	class Meta:
		model = BorrowerInfoRequest 
		fields = '__all__'
		
'''class AccountForm(forms.ModelForm):
	class Meta:
		model = Account
		fields = ['name_first', 'name_middle', 'name_last', 'phone', 'taxid', 'language', 'address']'''
		
'''class ExpenseInfoForm(forms.ModelForm):
	class Meta:
		model = ExpenseInfo
		fields = '__all__'	'''