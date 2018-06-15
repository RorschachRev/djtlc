from django import forms
from wwwtlc.models import Person, Wallet
from wwwtlc.models_loan_app import *

class WalletForm(forms.ModelForm):
	class Meta:
		model = Wallet
		fields = ['blockchain', 'address']	
		
'''class AccountForm(forms.ModelForm):
	class Meta:
		model = Account
		fields = ['name_first', 'name_middle', 'name_last', 'phone', 'taxid', 'language', 'address']'''
		
# Below are forms for the new models - correlates to models_loan_app.py

# models not listed in the forms, due to only needing to be accessed by staff:
#	- LenderInfo
#	- Loan Terms
#	- LoanWorkflow
#	- LoanSummary

class ConstructionInfoForm(forms.ModelForm):
	class Meta:
		model = ConstructionInfo
		fields = '__all__'
		
class RefinanceInfoForm(forms.ModelForm):
	class Meta:
		model = RefinanceInfo
		fields = '__all__'

class PropertyInfoForm(forms.ModelForm):
	class Meta:
		model = PropertyInfo
		fields = '__all__'	

class EmploymentIncomeForm(forms.ModelForm):
	class Meta:
		model = EmploymentIncome
		fields = '__all__'	
		
class BusinessInfoForm(forms.ModelForm):
	class Meta:
		model = BusinessInfo
		fields = '__all__'	
		
'''class ExpenseInfoForm(forms.ModelForm):
	class Meta:
		model = ExpenseInfo
		fields = '__all__'	'''

class BankAccountForm(forms.ModelForm):
	class Meta:
		model = BankAccount
		fields = '__all__'
		
class StockForm(forms.ModelForm):
	class Meta:
		model = Stock
		fields = '__all__'
		
class BondForm(forms.ModelForm):
	class Meta:
		model = Bond
		fields = '__all__'
		
class VehicleForm(forms.ModelForm):
	class Meta:
		model = Vehicle
		fields = '__all__'

class AssetSummaryForm(forms.ModelForm):
	class Meta:
		model = AssetSummary
		fields = '__all__'

class DebtForm(forms.ModelForm):
	class Meta:
		model = Debt
		fields = '__all__'

class AlimonyForm(forms.ModelForm):
	class Meta:
		model = Alimony
		fields = '__all__'

class ChildSupportForm(forms.ModelForm):
	class Meta:
		model = ChildSupport
		fields = '__all__'

class SeparateMaintForm(forms.ModelForm):
	class Meta:
		model = SeparateMaint
		fields = '__all__'

class ManagedPropertyForm(forms.ModelForm):
	class Meta:
		model = ManagedProperty
		fields = '__all__'
		
class LiabilitySummaryForm(forms.ModelForm):
	class Meta:
		model = LiabilitySummary
		fields = '__all__'

class ALSummaryForm(forms.ModelForm):
	class Meta:
		model = ALSummary
		fields = '__all__'		

class TransactionDetailsForm(forms.ModelForm):
	class Meta:
		model = TransactionDetails
		fields = '__all__'
		
class DeclarationForm(forms.ModelForm):
	class Meta:
		model = Declaration
		fields = '__all__'	

class BorrowerInfoForm(forms.ModelForm):
	class Meta:
		model = BorrowerInfo
		fields = '__all__'			

class AcknowledgeAgreeForm(forms.ModelForm):
	class Meta:
		model = AcknowledgeAgree
		fields = '__all__'
		
class CreditRequestForm(forms.ModelForm):
	class Meta:
		model = CreditRequest
		fields = '__all__'