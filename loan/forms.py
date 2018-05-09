from django import forms
from .models import Loan, Loan_Data

class LoanDataForm(forms.ModelForm):
	class Meta:
		model = Loan_Data
		fields = ['borrower_requested', 'borrower_type', 'contact_person', 'loan_partner', 'loan_address', 'loan_principle', 'loan_currency', 'loan_type']
		

class LoanForm(forms.ModelForm):
	class Meta:
		model = Loan
		fields = ['loan_payment_request']
		
		
# Below is form that doesn't connect to models :(
'''class LoanForm(forms.Form):
	LOAN_CHOICES = [
		(0, 'Fixed'),
		(1, 'ARM'),
		#(2, 'Shariah'),
	]
	
	borrower_requested = forms.CharField(label='Loan Borrower:', max_length=60)
	contact_person = forms.CharField(label='Contact Person:', max_length=60)
	loan_amount = forms.DecimalField(label='Loan Amount (USD):', min_value=0, decimal_places=4, max_digits=12)
	requested_payment = forms.DecimalField(label='Payment Request (USD):', min_value=.01, decimal_places=4, max_digits=12)
	loan_address = forms.CharField(label='Property Address:', max_length=100)
	loan_type = forms.CharField(label='Loan Type:', widget=forms.Select(choices=LOAN_CHOICES))'''
	