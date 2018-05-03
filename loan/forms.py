from django import forms

class LoanForm(forms.Form):
	user_id = forms.CharField(label='User ID:', max_length=100)
	wal_id = forms.CharField(label='Wallet ID:', max_length=30)
	loan_amt = forms.DecimalField(label='Loan Amount:', min_value=0.01, decimal_places=2)