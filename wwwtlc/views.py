#from wwwtlc.models import Person, Loan, Loan_Data
from wwwtlc.models import Person, Wallet
from loan.models import Loan, Loan_Data
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
def payhistory(request):
	loaninfo.wallet_addr='303f9e7D8588EC4B1464252902d9e2a96575168A'
	blockdata=BC()
	blockdata.loanbal=blockdata.get_loan_bal(loaninfo.wallet_addr) / 100	
	return render(request, 'pages/payhistory.html', {'loan': loaninfo, 'blockdata':blockdata })

def home(request):
	return render(request, 'pages/home.html')
	
# This is the old loan.html view
'''def loan(request):
#TODO: fetch all loans for user
	loaninfo.wallet_addr=str(Loan.objects.all().filter(user=request.user)) #'303f9e7D8588EC4B1464252902d9e2a96575168A'
	blockdata=BC()
	blockdata.loanbal=blockdata.get_loan_bal(loaninfo.wallet_addr) / 100
#	loaninfo.payment=Loan.loan_payment_required
	loaninfo.payment=D.Decimal(Loan.objects.all().filter(user=request.user)) #previously hardcoded as 5000
	blockdata.tlctousdc=D.Decimal(blockdata.get_TLC_USDc() ) / 100000000 
	loaninfo.payTLC= loaninfo.payment / blockdata.tlctousdc
	return render(request, 'pages/loan.html', {'loan': loaninfo, 'blockdata':blockdata })'''
	
# New view in testing
def loan(request):
	loan_iterable = Loan.objects.all().filter(user=request.user) #used to display all loans to be called in loan.html
	blockdata=BC() #not sure what to do with this
	
	loaninfo.wallet_addr = str(Loan.objects.all().filter(user=request.user)) #sets the wallet address in loaninfo
	blockdata.loanbal= blockdata.get_loan_bal(loaninfo.wallet_addr) / 100 #sets balance associated with loaninfo.wallet
	loaninfo.payment = Loan.objects.values_list('loan_payment_due') #sets the amount of money that they owe for every payment in loaninfo
	blockdata.tlctousdc= D.Decimal(blockdata.get_TLC_USDc() ) / 100000000
	#loaninfo.payTLC= loaninfo.payment / blockdata.tlctousdc #don't know what to do with this, it breaks: "error: unsupported operand type(s) for /: 'QuerySet' and 'decimal.Decimal'
	
	return render(request, 'pages/loan.html', {'loan': loaninfo, 'blockdata': blockdata, 'loan_iterable': loan_iterable}) #added loan_iterable to display info in loan.html w/ for loop
	
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
	
def pay(request, loan_id):
#TODO: select loan by ID
	loaninfo.wallet_addr= str(Loan.objects.get(pk=loan_id).loan_wallet.address)
	blockdata=BC()
	blockdata.loanbal= Loan.objects.get(pk=loan_id).loan_balance#D.Decimal(blockdata.get_loan_bal(x)) #commented b/c blockdata.get_loan_bal overwrites Loan.objects.get(pk=loan_id).loan_balance and sets it to 0
	loaninfo.payment=Loan.objects.get(pk=loan_id).loan_payment_due
	blockdata.tlctousdc=D.Decimal(blockdata.get_TLC_USDc() ) / 100000000 
	loaninfo.payTLC= loaninfo.payment / blockdata.tlctousdc
	return render(request, 'pages/pay.html', {'loan': loaninfo, 'blockdata':blockdata} )
	
def test(request):
	return render(request, 'pages/test.html')
	
