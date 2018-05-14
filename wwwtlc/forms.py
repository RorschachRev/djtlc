from django import forms
from wwwtlc.models import Person, Wallet

class WalletForm(forms.ModelForm):
	class Meta:
		model = Wallet
		fields = ['blockchain', 'address']	