from wwwtlc.models import Person, Wallet
from loan.models import Loan, Loan_Data
from django.conf import settings
from loan.forms import PersonEditForm, PersonForm
from django import forms
from django.shortcuts import render, get_object_or_404, HttpResponseRedirect
from wwwtlc.ethereum import BC
import decimal as D
from wwwtlc.forms import *
from formtools.wizard.views import CookieWizardView #SessionWizardView # commented out to test save-every-step strategy

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

# These views implement the save on every step strategy, this was done originally but
# was removed and replaced due to saving form once on every step and once at the end.
# reimplemented due to session/serialize data testing
'''
# Original formview double save:
# https://github.com/RorschachRev/djtlc/commit/fc0e30e977f45729a38624e50fa4250d4763c900

# Updated save-at end formview:
# https://github.com/RorschachRev/djtlc/commit/ae009f0386159be9732cc75c835d0f6efe9a3991
'''
class TierOneWizard(CookieWizardView):
	def get_form(self, step=None, data=None, files=None):
		form = super(TierOneWizard, self).get_form(step, data, files)
	
		if step is None:
			step = self.steps.current
			print('\n#### self.steps.current ####')
		if step == '0':
			if form.is_valid():
				print('#### step 0: Valid ####\n')
				form.save()
		if step == '1':
			if form.is_valid():
				print('#### step 1: Valid ####\n')
				form.save()
		if step == '2':
			if form.is_valid():
				print('#### step 2: Valid ####\n')
				form.save()
		if step == '3':
			if form.is_valid():
				print('#### step 3: Valid ####\n')
				form.save()
		if step == '4':
			if form.is_valid():
				print('#### step 4: Valid ####\n')
				form.save()
		if step == '5':
			if form.is_valid():
				print('#### step 5: Valid ####\n')
				form.save()
		if step == '6':
			if form.is_valid():
				print('#### step 6: Valid ####\n')
				form.save()
		if step == '7':
			if form.is_valid():
				print('#### step 7: Valid ####\n')
				form.save()
		if step == '8':
			if form.is_valid():
				print('#### step 8: Valid ####\n')
				form.save()
			
		return form
	
	def done(self, form_list, **kwargs):
		return HttpResponseRedirect('loan_apply_done.html')
		
class TierTwoWizard(CookieWizardView):
	def get_form(self, step=None, data=None, files=None):
		form = super(TierTwoWizard, self).get_form(step, data, files)
		
		if step is None:
			step = self.steps.current
			print('\n#### self.steps.current ####')
		if step == '0':
			if form.is_valid():
				print('#### step 0: Valid ####\n')
				form.save()
		if step == '1':
			if form.is_valid():
				print('#### step 1: Valid ####\n')
				form.save()
		if step == '2':
			if form.is_valid():
				print('#### step 2: Valid ####\n')
				form.save()
		if step == '3':
			if form.is_valid():
				print('#### step 3: Valid ####\n')
				form.save()
		if step == '4':
			if form.is_valid():
				print('#### step 4: Valid ####\n')
				form.save()
		if step == '5':
			if form.is_valid():
				print('#### step 5: Valid ####\n')
				form.save()
		if step == '6':
			if form.is_valid():
				print('#### step 6: Valid ####\n')
				form.save()
		if step == '7':
			if form.is_valid():
				print('#### step 7: Valid ####\n')
				form.save()
		if step == '8':
			if form.is_valid():
				print('#### step 8: Valid ####\n')
				form.save()
		if step == '9':
			if form.is_valid():
				print('#### step 9: Valid ####\n')
				form.save()
		if step == '10':
			if form.is_valid():
				print('#### step 10: Valid ####\n')
				form.save()
		if step == '11':
			if form.is_valid():
				print('#### step 11: Valid ####\n')
				form.save()
		if step == '12':
			if form.is_valid():
				print('#### step 12: Valid ####\n')
				form.save()
		if step == '13':
			if form.is_valid():
				print('#### step 13: Valid ####\n')
				form.save()
		if step == '14':
			if form.is_valid():
				print('#### step 14: Valid ####\n')
				form.save()
		if step == '15':
			if form.is_valid():
				print('#### step 15: Valid ####\n')
				form.save()
		if step == '16':
			if form.is_valid():
				print('#### step 16: Valid ####\n')
				form.save()
		if step == '17':
			if form.is_valid():
				print('#### step 17: Valid ####\n')
				form.save()
		if step == '18':
			if form.is_valid():
				print('#### step 18: Valid ####\n')
				form.save()
		if step == '19':
			if form.is_valid():
				print('#### step 19: Valid ####\n')
				form.save()
		if step == '20':
			if form.is_valid():
				print('#### step 20: Valid ####\n')
				form.save()
		if step == '21':
			if form.is_valid():
				print('#### step 21: Valid ####\n')
				form.save()
			
		return form
		
	def done(self, form_list, **kwargs):
		return HttpResponseRedirect('loan_apply_done.html')

# Below are working views that handle saving form data at end of form process
# commented out to pursue session/serialize data handling - 7.2.18
'''class TierOneWizard(SessionWizardView):

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
			e = self.get_form(step='4', data=e_data).save(commit=False)
			f = self.get_form(step='5', data=f_data).save()
			g = self.get_form(step='6', data=g_data).save()
			h = self.get_form(step='7', data=h_data).save()
			i = self.get_form(step='8', data=i_data).save()
			
			# Sets BorrowerInfo.user = currently logged in user
			e.user = self.request.user
			e.save()
			
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
		# j, 9 = Asset Summary
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
			r = self.get_form(step='17', data=r_data).save(commit=False)
			s = self.get_form(step='18', data=s_data).save()
			t = self.get_form(step='19', data=t_data).save()
			u = self.get_form(step='20', data=u_data).save()
			v = self.get_form(step='21', data=v_data).save()
			
			# Sets BorrowerInfo.user = currently logged in user
			r.user = self.request.user
			r.save()
			
		return render(self.request, 'pages/loan_apply_done.html')'''