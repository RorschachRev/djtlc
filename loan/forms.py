from django import forms

class LoanForm(forms.Form):
	user_id = forms.CharField(label='User ID:', max_length=100)