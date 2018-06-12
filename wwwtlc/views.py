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
def loanappnew(request):
	form = CreditRequestedForm(request.POST)
	form1 = ApplicantInfoForm(request.POST)
	form2 = CollateralScheduleForm(request.POST)
	#form3 = AssetScheduleForm(request.POST)
	#form4 = LiabilityScheduleForm(request.POST)
	#form5 = ExpenseScheduleForm(request.POST)
	#form6 = IncomeScheduleForm(request.POST)
	#form7 = FinanceSummaryForm(request.POST)
	form8 = RelationshipInfoForm(request.POST)
	#form9 = ApplicantSignersForm(request.POST)
	#form10 = ApplicantSignaturesForm(request.POST)
	form11 = LenderInfoForm(request.POST)
	
	context = {
		'form':form,
		'form1':form1,
		'form2':form2,
		#'form3':form3,
		#'form4':form4,
		#'form5':form5,
		#'form6':form6,
		#'form7':form7,
		'form8':form8,
		#'form9':form9,
		#'form10':form10,
		'form11':form11,
	}
	
	return render(request, 'pages/loan_app1.html', context)
	
def loanappnew2(request):
	form = LoanTermsForm(request.POST)
	form1 = ConstructionInfoForm(request.POST)
	form2 = RefinanceInfoForm(request.POST)
	form3 = PropertyInfoForm(request.POST)
	form4 = EmploymentInfoForm(request.POST)
	form5 = IncomeInfoForm(request.POST)
	form6 = ExpenseInfoForm(request.POST)
	form7 = BankAccountForm(request.POST)
	form8 = StockForm(request.POST)
	form9 = BondForm(request.POST)
	form10 = VehicleForm(request.POST)
	form11 = AssetSummaryForm(request.POST)
	form12 = DebtForm(request.POST)
	form13 = AlimonyForm(request.POST)
	form14 = ChildSupportForm(request.POST)
	form15 = SeparateMaintForm(request.POST)
	form16 = LiabilitySummaryForm(request.POST)
	form17 = ALSummaryForm(request.POST)
	form18 = DeclarationForm(request.POST)
	form19 = BorrowerInfoForm(request.POST)
	form20 = AcknowledgeAgreeForm(request.POST)
	
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
	}
	
	return render(request, 'pages/loan_app2.html', context)