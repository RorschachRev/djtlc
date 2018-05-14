#from wwwtlc.models import Person, Loan, Loan_Data
from wwwtlc.models import Person, Wallet
from django.conf import settings
from django.shortcuts import render, get_object_or_404
#from django.core.mail import send_mail
from django import forms
from wwwtlc.ethereum import BC
import decimal as D

class WalletForm(forms.ModelForm):
	class Meta:
		model = Wallet
		fields = ['address']	

class loaninfo():
	"""
	Stub for blockchain state. Will include config data later.
	"""
	def __init__(self):
		pass


def home(request):
	return render(request, 'pages/home.html')
def loan(request):
	loaninfo.wallet_addr='303f9e7D8588EC4B1464252902d9e2a96575168A'
	blockdata=BC()
	blockdata.loanbal=blockdata.get_loan_bal(loaninfo.wallet_addr)
	loaninfo.payment=D.Decimal(5000)
	blockdata.tlctousdc=D.Decimal(blockdata.get_TLC_USDc() ) / 100000000 
	loaninfo.payTLC= loaninfo.payment / blockdata.tlctousdc
	return render(request, 'pages/loan.html', {'loan': loaninfo, 'blockdata':blockdata })
def wallet(request):
	if request.method == 'POST':
		form = WalletForm(request.POST)
		if form.is_valid():
			obj=form.save(commit=False)
			obj.wallet=request.user
			obj.blockchain="ETH"
			obj.save()
	w=Wallet.objects.all().filter(wallet=request.user)
	form=WalletForm()
	return render(request, 'pages/wallet.html', {'wallet': w, 'form':form })
def pay(request):
	loaninfo.wallet_addr='303f9e7D8588EC4B1464252902d9e2a96575168A'
	blockdata=BC()
	blockdata.loanbal=blockdata.get_loan_bal(loaninfo.wallet_addr)
	loaninfo.payment=D.Decimal(5000)
	blockdata.tlctousdc=D.Decimal(blockdata.get_TLC_USDc() ) / 100000000 
	loaninfo.payTLC= loaninfo.payment / blockdata.tlctousdc
	return render(request, 'pages/pay.html', {'loan': loaninfo, 'blockdata':blockdata} )
def test(request):
	return render(request, 'pages/test.html')
	
