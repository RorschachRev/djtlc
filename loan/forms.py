from django import forms

class LoanForm(forms.Form):
	borrower_id = forms.CharField(label='Borrower ID:')
	contact_person_id = forms.CharField(label='Contact Person ID:')
	loan_officer_id = forms.CharField(label='Loan Officer ID:')
	loan_amt = forms.DecimalField(label='Loan Amount:', min_value=0, decimal_places=2)
	loan_payment_monthly = forms.DecimalField(label='Monthly Payment:', decimal_places=2)
	drop_down = forms.ChoiceField(choices=[(x, x) for x in range(1, 32)])