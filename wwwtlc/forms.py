from django import forms
from wwwtlc.models import Person, Wallet

class WalletForm(forms.ModelForm):
	class Meta:
		model = Wallet
		fields = ['blockchain', 'address']	
class AccountForm(forms.ModelForm):
	class Meta:
		model = Account
		fields = ['name_first', 'name_middle', 'name_last', 'phone', 'taxid', 'language', 'address']