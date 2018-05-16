from django import forms
from .models import Loan, Loan_Data
from wwwtlc.models import Address, Person

# deleted from forms :
# 	loan_data = contact_person, loan_address
#	person = address
#
# These were deleted from the forms so that the formWizard would not prompt the user to enter that data, and instead just set that data based on information in previous form step
class LoanDataForm(forms.ModelForm):
	class Meta:
		model = Loan_Data
		fields = ['borrower_requested', 'borrower_type', 'loan_principle', 'loan_currency', 'loan_type']
		

class LoanForm(forms.ModelForm):
	class Meta:
		model = Loan
		fields = ['loan_payment_request']
		
class AddressForm(forms.ModelForm):
	class Meta:
		model = Address
		fields = ['street1', 'street2', 'street3', 'city', 'state', 'zipcode', 'country']
		
class PersonForm(forms.ModelForm):
	class Meta:
		model = Person
		fields = ['name_first', 'name_middle', 'name_last', 'phone', 'taxid', 'language']	