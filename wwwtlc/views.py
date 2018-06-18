from wwwtlc.models import Person, Wallet
from loan.models import Loan, Loan_Data
from django.conf import settings
from loan.forms import PersonEditForm, PersonForm
from django import forms
from django.shortcuts import render, get_object_or_404
from wwwtlc.ethereum import BC
import decimal as D
from wwwtlc.forms import *
from formtools.wizard.views import SessionWizardView

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

# Django FormWizard view for Tier 1
# (BizInfo -> ConstrInfo -> RefineInfo -> PropInfo -> BorrowerInfo -> CreditReq -> Decl -> Transaction -> Agree)
class TierOneWizard(SessionWizardView):
	def done(self, form_list, **kwargs):
		# a, 0 = BusinessInfo
		# b, 1 = ConstructionInfo
		# c, 2 = RefinanceInfo
		# d, 3 = PropertyInfo
		# e, 4 = BorrowerInfo
		# f, 5 = CreditRequest
		# g, 6 = Declaration
		# h, 7 = TransactionDetails
		# i, 8 = AcknowledgeAgree
		
		# This block of code retrieves data and binds it to the form fields, then validates each step
		a_data = self.storage.get_step_data('0')
		a_valid = self.get_form(step='0', data=a_data).is_valid()
		b_data = self.storage.get_step_data('1')
		b_valid = self.get_form(step='1', data=b_data).is_valid()
		c_data = self.storage.get_step_data('2')
		c_valid = self.get_form(step='2', data=c_data).is_valid()
		d_data = self.storage.get_step_data('3')
		d_valid = self.get_form(step='3', data=d_data).is_valid()
		e_data = self.storage.get_step_data('4')
		e_valid = self.get_form(step='4', data=e_data).is_valid()
		f_data = self.storage.get_step_data('5')
		f_valid = self.get_form(step='5', data=f_data).is_valid()
		g_data = self.storage.get_step_data('6')
		g_valid = self.get_form(step='6', data=g_data).is_valid()
		h_data = self.storage.get_step_data('7')
		h_valid = self.get_form(step='7', data=h_data).is_valid()
		i_data = self.storage.get_step_data('8')
		i_valid = self.get_form(step='8', data=i_data).is_valid()
		
		if (
			a_valid and b_valid and c_valid
			and d_valid and e_valid and f_valid
			and g_valid and h_valid and i_valid
		):
			a = self.get_form(step='0', data=a_data).save()
			b = self.get_form(step='1', data=b_data).save()
			c = self.get_form(step='2', data=c_data).save()
			d = self.get_form(step='3', data=d_data).save()
			e = self.get_form(step='4', data=e_data).save()
			f = self.get_form(step='5', data=f_data).save()
			g = self.get_form(step='6', data=g_data).save()
			h = self.get_form(step='7', data=h_data).save()
			i = self.get_form(step='8', data=i_data).save()
			
		return render(self.request, 'pages/loan_apply_done.html')
			
# Django FormWizard view for Tier 2
# (BizInfo -> ConstInfo -> RefineInfo -> PropInfo -> EmpIncInfo -> Bank -> Bond -> Stock ->
#	Vehicle -> Asset -> Debt -> Manage -> Ali -> Child -> Seperate -> Liability -> A&L ->
#	Borrow -> CreditReq -> Declare -> Transact -> Acknowledge)
class TierTwoWizard(SessionWizardView):
	def done(self, form_list, **kwargs):
		# a, 0 = BusinessInfo
		# b, 1 = ConstructionInfo
		# c, 2 = RefinanceInfo
		# d, 3 = PropertyInfo
		# e, 4 = EmploymentIncomeInfo
		# f, 5 = BankAccount
		# g, 6 = Bond
		# h, 7 = Stock
		# i, 8 = Vehicle
		# j, 9 = Asset
		# k, 10 = Debt
		# l, 11 = ManagedProperty
		# m, 12 = Alimony
		# n, 13 = ChildSupport
		# o, 14 = SeperateMaintenance
		# p, 15 = LiabilitySummary
		# q, 16 = ALSummary
		# r, 17 = BorrowerInformation
		# s, 18 = CreditRequest
		# t, 19 = Declaration
		# u, 20 = TransactionDetails
		# v, 21 = AcknowledgeAgree
		
		# This block of code retrieves data and binds it to the form fields, then validates each step
		a_data = self.storage.get_step_data('0')
		a_valid = self.get_form(step='0', data=a_data).is_valid()
		b_data = self.storage.get_step_data('1')
		b_valid = self.get_form(step='1', data=b_data).is_valid()
		c_data = self.storage.get_step_data('2')
		c_valid = self.get_form(step='2', data=c_data).is_valid()
		d_data = self.storage.get_step_data('3')
		d_valid = self.get_form(step='3', data=d_data).is_valid()
		e_data = self.storage.get_step_data('4')
		e_valid = self.get_form(step='4', data=e_data).is_valid()
		f_data = self.storage.get_step_data('5')
		f_valid = self.get_form(step='5', data=f_data).is_valid()
		g_data = self.storage.get_step_data('6')
		g_valid = self.get_form(step='6', data=g_data).is_valid()
		h_data = self.storage.get_step_data('7')
		h_valid = self.get_form(step='7', data=h_data).is_valid()
		i_data = self.storage.get_step_data('8')
		i_valid = self.get_form(step='8', data=i_data).is_valid()
		j_data = self.storage.get_step_data('9')
		j_valid = self.get_form(step='9', data=j_data).is_valid()
		k_data = self.storage.get_step_data('10')
		k_valid = self.get_form(step='10', data=k_data).is_valid()
		l_data = self.storage.get_step_data('11')
		l_valid = self.get_form(step='11', data=l_data).is_valid()
		m_data = self.storage.get_step_data('12')
		m_valid = self.get_form(step='12', data=m_data).is_valid()
		n_data = self.storage.get_step_data('13')
		n_valid = self.get_form(step='13', data=n_data).is_valid()
		o_data = self.storage.get_step_data('14')
		o_valid = self.get_form(step='14', data=o_data).is_valid()
		p_data = self.storage.get_step_data('15')
		p_valid = self.get_form(step='15', data=p_data).is_valid()
		q_data = self.storage.get_step_data('16')
		q_valid = self.get_form(step='16', data=q_data).is_valid()
		r_data = self.storage.get_step_data('17')
		r_valid = self.get_form(step='17', data=r_data).is_valid()
		s_data = self.storage.get_step_data('18')
		s_valid = self.get_form(step='18', data=s_data).is_valid()
		t_data = self.storage.get_step_data('19')
		t_valid = self.get_form(step='19', data=t_data).is_valid()
		u_data = self.storage.get_step_data('20')
		u_valid = self.get_form(step='20', data=u_data).is_valid()
		v_data = self.storage.get_step_data('21')
		v_valid = self.get_form(step='21', data=v_data).is_valid()
		
		if (
			a_valid and b_valid and c_valid 
			and d_valid and e_valid and f_valid
			and g_valid and h_valid and i_valid
			and j_valid and k_valid and l_valid
			and m_valid and n_valid and o_valid
			and p_valid and q_valid and r_valid
			and s_valid and t_valid and u_valid
			and v_valid
		):
			a = self.get_form(step='0', data=a_data).save()
			b = self.get_form(step='1', data=b_data).save()
			c = self.get_form(step='2', data=c_data).save()
			d = self.get_form(step='3', data=d_data).save()
			e = self.get_form(step='4', data=e_data).save()
			f = self.get_form(step='5', data=f_data).save()
			g = self.get_form(step='6', data=g_data).save()
			h = self.get_form(step='7', data=h_data).save()
			i = self.get_form(step='8', data=i_data).save()
			j = self.get_form(step='9', data=j_data).save()
			k = self.get_form(step='10', data=k_data).save()
			l = self.get_form(step='11', data=l_data).save()
			m = self.get_form(step='12', data=m_data).save()
			n = self.get_form(step='13', data=n_data).save()
			o = self.get_form(step='14', data=o_data).save()
			p = self.get_form(step='15', data=p_data).save()
			q = self.get_form(step='16', data=q_data).save()
			r = self.get_form(step='17', data=r_data).save()
			s = self.get_form(step='18', data=s_data).save()
			t = self.get_form(step='19', data=t_data).save()
			u = self.get_form(step='20', data=u_data).save()
			v = self.get_form(step='21', data=v_data).save()
			
		return render(self.request, 'pages/loan_apply_done.html')

# below are old views, commented out to implement FormWizard multi-step form
'''def tier1(request):
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
	
	return render(request, 'pages/tier2_app.html', context)'''