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
class CreditRequestedForm(forms.ModelForm):
	class Meta:
		model = CreditRequested
		fields = '__all__'
		
class ApplicantInfoForm(forms.ModelForm):
	class Meta:
		model = ApplicantInfo
		fields = '__all__'

class CollateralScheduleForm(forms.ModelForm):
	class Meta:
		model = CollateralSchedule
		fields = '__all__'
		
class AssetScheduleForm(forms.ModelForm):
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
		fields = '__all__'

class RelationshipInfoForm(forms.ModelForm):
	class Meta:
		model = RelationshipInfo
		fields = '__all__'	

class ApplicantSignersForm(forms.ModelForm):
	class Meta:
		model = ApplicantSigners
		fields = '__all__'

class ApplicantSignaturesForm(forms.ModelForm):
	class Meta:
		model = ApplicantSignatures
		fields = '__all__'		

class LenderInfoForm(forms.ModelForm):
	class Meta:
		model = LenderInfo
		fields = '__all__'	

##########################################
# Below are forms for new models - correlates to models_loan_app2.py
class LoanTermsForm(forms.ModelForm):
	class Meta:
		model = LoanTerms
		fields = '__all__'	

class PropertyInfoForm(forms.ModelForm):
	class Meta:
		model = PropertyInfo
		fields = '__all__'

class BorrowerInfoForm(forms.ModelForm):
	class Meta:
		model = BorrowerInfo
		fields = '__all__'		

class EmploymentInfoForm(forms.ModelForm):
	class Meta:
		model = EmploymentInfo
		fields = '__all__'	
		
class IncomeExpenseInfoForm(forms.ModelForm):
	class Meta:
		model = IncomeExpenseInfo
		fields = '__all__'	

class AssetsLiabilitiesForm(forms.ModelForm):
	class Meta:
		model = AssetsLiabilities
		fields = '__all__'

class DeclarationsForm(forms.ModelForm):
	class Meta:
		model = Declarations
		fields = '__all__'		

class AcknowledgeAgreeForm(forms.ModelForm):
	class Meta:
		model = AcknowledgeAgree
		fields = '__all__'	