from django import forms
from .models import *
from wwwtlc.models_meta import *
from wwwtlc.models_loan_apply import *

# deleted from forms :
# 	loan_data = contact_person, loan_address
#	person = address
#
# These were deleted from the forms so that the formWizard would not prompt the user to enter that data, and instead just set that data based on information in previous form step
class LoanDataForm(forms.ModelForm):
	class Meta:
		model = Loan_Data
		fields = ['borrower_type', 'loan_currency', 'loan_type']
		
class LoanRequestForm(forms.ModelForm):
	class Meta:
		model = Loan_Request
		fields = ['borrower_requested', 'loan_request_amt', 'loan_payment_request', 'loan_intrate_request', 'loan_request_date']
		
class ChangeReqForm(forms.ModelForm):
	class Meta:
		model = NewRequestSummary
		fields = ['status']
		labels = {
			'status': '',
		}
		
class AddressForm(forms.ModelForm):
	class Meta:
		model = Address
		fields = ['street1', 'street2', 'street3', 'city', 'state', 'zipcode', 'country']
		
class PersonForm(forms.ModelForm):
	class Meta:
		model = Person
		fields = ['name_first', 'name_middle', 'name_last', 'phone', 'email_address']

class PersonEditForm(forms.ModelForm):
	class Meta:
		model = Person
		fields = ['name_first', 'name_middle', 'name_last', 'phone', 'language']		