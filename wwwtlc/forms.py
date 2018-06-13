from django import forms
from wwwtlc.models import Person, Wallet
from wwwtlc.models_loan_app import *
from wwwtlc.models_loan_app2 import *

class WalletForm(forms.ModelForm):
	class Meta:
		model = Wallet
		fields = ['blockchain', 'address']	
		
'''class AccountForm(forms.ModelForm):
	class Meta:
		model = Account
		fields = ['name_first', 'name_middle', 'name_last', 'phone', 'taxid', 'language', 'address']'''
		
# Below are forms for the new models - correlates to models_loan_app.py
class CreditRequestForm(forms.ModelForm):
	class Meta:
		model = CreditRequest
		fields = '__all__'
		
'''class ApplicantInfoForm(forms.ModelForm):
	class Meta:
		model = ApplicantInfo
		fields = '__all__'''

class CollateralScheduleForm(forms.ModelForm):
	class Meta:
		model = CollateralSchedule
		fields = '__all__'

class RelationshipInfoForm(forms.ModelForm):
	class Meta:
		model = RelationshipInfo
		fields = '__all__'

class LenderInfoForm(forms.ModelForm):
	class Meta:
		model = LenderInfo
		fields = '__all__'	
		
# below block of forms may have models that will be removed, so they've been commented out
'''class AssetScheduleForm(forms.ModelForm):
	class Meta:
		model = AssetSchedule
		fields = '__all__'

class LiabilityScheduleForm(forms.ModelForm):
	class Meta:
		model = LiabilitySchedule
		fields = '__all__'

class ExpenseScheduleForm(forms.ModelForm):
	class Meta:
		model = ExpenseSchedule
		fields = '__all__'

class IncomeScheduleForm(forms.ModelForm):
	class Meta:
		model = IncomeSchedule
		fields = '__all__'	

class FinanceSummaryForm(forms.ModelForm):
	class Meta:
		model = FinanceSummary
		fields = '__all__'''	

'''class ApplicantSignersForm(forms.ModelForm):
	class Meta:
		model = ApplicantSigners
		fields = '__all__'''	

##########################################
# Below are forms for new models - correlates to models_loan_app2.py
class LoanTermsForm(forms.ModelForm):
	class Meta:
		model = LoanTerms
		fields = '__all__'

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

class EmploymentInfoForm(forms.ModelForm):
	class Meta:
		model = EmploymentInfo
		fields = '__all__'	
		
class IncomeInfoForm(forms.ModelForm):
	class Meta:
		model = IncomeInfo
		fields = '__all__'	
		
class ExpenseInfoForm(forms.ModelForm):
	class Meta:
		model = ExpenseInfo
		fields = '__all__'	

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

class LiabilitySummaryForm(forms.ModelForm):
	class Meta:
		model = LiabilitySummary
		fields = '__all__'

class ALSummaryForm(forms.ModelForm):
	class Meta:
		model = ALSummary
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