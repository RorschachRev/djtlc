from wwwtlc.models import Person, Wallet
from loan.models import Loan, Loan_Data
from django.conf import settings
from loan.forms import PersonEditForm, PersonForm
from django import forms
from django.shortcuts import render, get_object_or_404
from wwwtlc.ethereum import BC
import decimal as D
from wwwtlc.forms import *

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
	
def loan(request):
	loan_iterable = Loan.objects.all().filter(user=request.user)
	blockdata=BC()
	return render(request, 'pages/loan.html', {'loan_iterable': loan_iterable, 'blockdata': blockdata})
	
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
	
# this function selects a specific loan associated with the user and displays just that one	
def pay(request, loan_id):
	loaninfo.wallet_addr= str(Loan.objects.get(pk=loan_id).loan_wallet.address)
	blockdata=BC()
	blockdata.loanbal=blockdata.get_loan_bal(loaninfo.wallet_addr) / 100
	loaninfo.payment=Loan.objects.get(pk=loan_id).loan_payment_due
	blockdata.tlctousdc=D.Decimal(blockdata.get_TLC_USDc() ) / 100000000 
	loaninfo.payTLC= loaninfo.payment / blockdata.tlctousdc
	return render(request, 'pages/pay.html', {'loan': loaninfo, 'blockdata':blockdata} )
	
def test(request):
	return render(request, 'pages/test.html')
	
#needs more testing with multiple different users.
def account(request):
	user = request.user
	try:
		acct_info = Person.objects.get(user=user)
		if request.method == 'POST':
			form = PersonEditForm(request.POST, instance=acct_info)
			if form.is_valid():
				form.save()
		else:
			form = PersonEditForm(instance=acct_info)
	except:
		form = PersonForm()
	return render(request, 'pages/account.html', {'form': form})
	
# BELOW IS NEW MODEL FORM INTEGRATION
def tier1(request):
	if request.method == 'POST':
		form = BusinessInfoForm(request.POST)
		form1 = ConstructionInfoForm(request.POST)
		form2 = RefinanceInfoForm(request.POST)
		form3 = PropertyInfoForm(request.POST)
		form4 = BorrowerInfoForm(request.POST)
		form5 = CreditRequestForm(request.POST)
		form6 = DeclarationForm(request.POST)
		form7 = TransactionDetailsForm(request.POST)
		form8 = AcknowledgeAgreeForm(request.POST)
		if ( 
			form.is_valid() and form1.is_valid() and form2.is_valid() 
			and form3.is_valid() and form4.is_valid() and form5.is_valid() 
			and form6.is_valid() and form7.is_valid() and form8.is_valid()
		):
			form.save()
			form1.save()
			form2.save()
			form3.save()
			form4.save()
			form5.save()
			form6.save()
			form7.save()
			form8.save()
	else:
		form = BusinessInfoForm()
		form1 = ConstructionInfoForm()
		form2 = RefinanceInfoForm()
		form3 = PropertyInfoForm()
		form4 = BorrowerInfoForm()
		form5 = CreditRequestForm()
		form6 = DeclarationForm()
		form7 = TransactionDetailsForm()
		form8 = AcknowledgeAgreeForm()
	
	context = {
		'form':form,
		'form1':form1,
		'form2':form2,
		'form3':form3,
		'form4':form4,
		'form5':form5,
		'form6':form6,
		'form7':form7,
		'form8':form8,
	}
	
	return render(request, 'pages/tier1_app.html', context)
	
# Tier 2 includes all fields required in Tier 1, plus additional fields not required in Tier 1,	\
# such as Asset and Liability information
def tier2(request):
	if request.method == 'POST':
		form = BusinessInfoForm(request.POST)
		form1 = ConstructionInfoForm(request.POST)
		form2 = RefinanceInfoForm(request.POST)
		form3 = PropertyInfoForm(request.POST)
		form4 = EmploymentIncomeForm(request.POST)
		form5 = BankAccountForm(request.POST)
		form6 = BondForm(request.POST)
		form7 = StockForm(request.POST)
		form8 = VehicleForm(request.POST)
		form9 = AssetSummaryForm(request.POST)
		form10 = DebtForm(request.POST)
		form11 = ManagedPropertyForm(request.POST)
		form12 = AlimonyForm(request.POST)
		form13 = ChildSupportForm(request.POST)
		form14 = SeparateMaintForm(request.POST)
		form15 = LiabilitySummaryForm(request.POST)
		form16 = ALSummaryForm(request.POST)
		form17 = BorrowerInfoForm(request.POST)
		form18 = CreditRequestForm(request.POST)
		form19 = DeclarationForm(request.POST)
		form20 = TransactionDetailsForm(request.POST)
		form21 = AcknowledgeAgreeForm(request.POST)
		if (
			form.is_valid() and form1.is_valid() and form2.is_valid() 
			and form3.is_valid() and form4.is_valid() and form5.is_valid() 
			and form6.is_valid() and form7.is_valid() and form8.is_valid() 
			and form9.is_valid() and form10.is_valid() and form11.is_valid() 
			and form12.is_valid() and form13.is_valid() and form14.is_valid() 
			and form15.is_valid() and form16.is_valid() and form17.is_valid() 
			and form18.is_valid() and form19.is_valid() and form20.is_valid() 
			and form21.is_valid()
		):
			form.save()
			form1.save()
			form2.save()
			form3.save()
			form4.save()
			form5.save()
			form6.save()
			form7.save()
			form8.save()
			form9.save()
			form10.save()
			form11.save()
			form12.save()
			form13.save()
			form14.save()
			form15.save()
			form16.save()
			form17.save()
			form18.save()
			form19.save()
			form20.save()
			form21.save()
	else:
		form = BusinessInfoForm()
		form1 = ConstructionInfoForm()
		form2 = RefinanceInfoForm()
		form3 = PropertyInfoForm()
		form4 = EmploymentIncomeForm()
		form5 = BankAccountForm()
		form6 = BondForm()
		form7 = StockForm()
		form8 = VehicleForm()
		form9 = AssetSummaryForm()
		form10 = DebtForm()
		form11 = ManagedPropertyForm()
		form12 = AlimonyForm()
		form13 = ChildSupportForm()
		form14 = SeparateMaintForm()
		form15 = LiabilitySummaryForm()
		form16 = ALSummaryForm()
		form17 = BorrowerInfoForm()
		form18 = CreditRequestForm()
		form19 = DeclarationForm()
		form20 = TransactionDetailsForm()
		form21 = AcknowledgeAgreeForm()

	context = {
		'form':form,
		'form1':form1,
		'form2':form2,
		'form3':form3,
		'form4':form4,
		'form5':form5,
		'form6':form6,
		'form7':form7,
		'form8':form8,
		'form9':form9,
		'form10':form10,
		'form11':form11,
		'form12':form12,
		'form13':form13,
		'form14':form14,
		'form15':form15,
		'form16':form16,
		'form17':form17,
		'form18':form18,
		'form19':form19,
		'form20':form20,
		'form21':form21,
	}
	
	return render(request, 'pages/tier2_app.html', context)