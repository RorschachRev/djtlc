from django import forms
from django.shortcuts import render, get_object_or_404, HttpResponseRedirect
from django.conf import settings
from django.core.mail import send_mail

import decimal as D

from wwwtlc.models import Person, Wallet
from wwwtlc.ethereum import BC
from wwwtlc.forms import *

from loan.models import Loan, Loan_Data
from loan.forms import PersonEditForm, PersonForm

from formtools.wizard.views import NamedUrlSessionWizardView

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
	
# Views for Loan Officer Dashboard - currently just template rendering, no data handling
def dashboard(request):
	return render(request, 'dashboard/dashboard.html', {})
	
def merge_requests(request):
	return render(request, 'dashboard/merge_request.html', {})
	
def workflow(request):
	return render(request, 'dashboard/workflow.html', {})
	
def credit_verify(request):
	return render(request, 'dashboard/credit_verify.html', {})
	
def package_loan(request):
	return render(request, 'dashboard/package_loan.html', {})
	
def manage_loan(request):
	return render(request, 'dashboard/manage_loan.html', {})
	
def loan_payments(request):
	return render(request, 'dashboard/loan_payments.html', {})
	
def payment_history(request):
	return render(request, 'dashboard/payment_history.html', {})
	
def loan_accounting(request):
	return render(request, 'dashboard/loan_accounting.html', {})
	
# Original Dashboard Views - Deprecated
'''def new_apps(request):
	return render(request, 'dashboard/new_apps.html', {})
	
def in_progress_apps(request):
	return render(request, 'dashboard/in_progress_apps.html', {})
	
def overdue(request):
	return render(request, 'dashboard/overdue.html', {})
	
def dashboard_loans(request):
	return render(request, 'dashboard/loans.html', {})
	
def loan_details(request):
	# this is where we query models to pull up information to plug into the template
	# use pay() above as an example for this snippet
	return render(request, 'dashboard/loan_details.html', {})'''
	
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
class TierOneWizard(NamedUrlSessionWizardView):
	def done(self, form_list, **kwargs):
		# a, 1 = BusinessInfo
		# b, 2 = ConstructionInfo
		# c, 3 = RefinanceInfo
		# d, 4 = PropertyInfo
		# e, 5 = BorrowerInfo
		# f, 6= CreditRequest
		# g, 7 = Declaration
		# h, 8 = TransactionDetails
		# i, 9 = AcknowledgeAgree
		
		# This block of code retrieves data and binds it to the form fields, then validates each step
		a_data = self.storage.get_step_data('1')
		a_valid = self.get_form(step='1', data=a_data).is_valid()
		b_data = self.storage.get_step_data('2')
		b_valid = self.get_form(step='2', data=b_data).is_valid()
		c_data = self.storage.get_step_data('3')
		c_valid = self.get_form(step='3', data=c_data).is_valid()
		d_data = self.storage.get_step_data('4')
		d_valid = self.get_form(step='4', data=d_data).is_valid()
		e_data = self.storage.get_step_data('5')
		e_valid = self.get_form(step='5', data=e_data).is_valid()
		f_data = self.storage.get_step_data('6')
		f_valid = self.get_form(step='6', data=f_data).is_valid()
		g_data = self.storage.get_step_data('7')
		g_valid = self.get_form(step='7', data=g_data).is_valid()
		h_data = self.storage.get_step_data('8')
		h_valid = self.get_form(step='8', data=h_data).is_valid()
		i_data = self.storage.get_step_data('9')
		i_valid = self.get_form(step='9', data=i_data).is_valid()
		
		if (
			a_valid and b_valid and c_valid
			and d_valid and e_valid and f_valid
			and g_valid and h_valid and i_valid
		):
			a = self.get_form(step='1', data=a_data).save()
			b = self.get_form(step='2', data=b_data).save()
			c = self.get_form(step='3', data=c_data).save()
			d = self.get_form(step='4', data=d_data).save()
			e = self.get_form(step='5', data=e_data).save(commit=False)
			f = self.get_form(step='6', data=f_data).save()
			g = self.get_form(step='7', data=g_data).save()
			h = self.get_form(step='8', data=h_data).save()
			i = self.get_form(step='9', data=i_data).save()
			
			# Sets BorrowerInfo.user = currently logged in user
			e.user = self.request.user
			e.save()
			
			# Sends email when data is submitted to DB
			send_mail(
				'A new loan has been submitted', # subject line - will change to add more info
				'This is where the application details will go', # message - will add more info to this
				'noreply@tlc.com', # 'from' email address
				['loanofficer@tlc.com'] # recipient email address
			)
			
		return render(self.request, 'pages/loan_apply_done.html')
		
class TierTwoWizard(NamedUrlSessionWizardView):
	def done(self, form_list, **kwargs):
		# a, 1 = BusinessInfo
		# b, 2 = ConstructionInfo
		# c, 3 = RefinanceInfo
		# d, 4 = PropertyInfo
		# e, 5 = EmploymentIncomeInfo
		# f, 6 = BankAccount
		# g, 7 = Bond
		# h, 8 = Stock
		# i, 9 = Vehicle
		# j, 10 = Asset Summary
		# k, 11 = Debt
		# l, 12 = ManagedProperty
		# m, 13 = Alimony
		# n, 14 = ChildSupport
		# o, 15 = SeperateMaintenance
		# p, 16 = LiabilitySummary
		# q, 17 = ALSummary
		# r, 18 = BorrowerInformation
		# s, 19 = CreditRequest
		# t, 20 = Declaration
		# u, 21 = TransactionDetails
		# v, 22 = AcknowledgeAgree
		
		# This block of code retrieves data and binds it to the form fields, then validates each step
		a_data = self.storage.get_step_data('1')
		a_valid = self.get_form(step='1', data=a_data).is_valid()
		b_data = self.storage.get_step_data('2')
		b_valid = self.get_form(step='2', data=b_data).is_valid()
		c_data = self.storage.get_step_data('3')
		c_valid = self.get_form(step='3', data=c_data).is_valid()
		d_data = self.storage.get_step_data('4')
		d_valid = self.get_form(step='4', data=d_data).is_valid()
		e_data = self.storage.get_step_data('5')
		e_valid = self.get_form(step='5', data=e_data).is_valid()
		f_data = self.storage.get_step_data('6')
		f_valid = self.get_form(step='6', data=f_data).is_valid()
		g_data = self.storage.get_step_data('7')
		g_valid = self.get_form(step='7', data=g_data).is_valid()
		h_data = self.storage.get_step_data('8')
		h_valid = self.get_form(step='8', data=h_data).is_valid()
		i_data = self.storage.get_step_data('9')
		i_valid = self.get_form(step='9', data=i_data).is_valid()
		j_data = self.storage.get_step_data('10')
		j_valid = self.get_form(step='10', data=j_data).is_valid()
		k_data = self.storage.get_step_data('11')
		k_valid = self.get_form(step='11', data=k_data).is_valid()
		l_data = self.storage.get_step_data('12')
		l_valid = self.get_form(step='12', data=l_data).is_valid()
		m_data = self.storage.get_step_data('13')
		m_valid = self.get_form(step='13', data=m_data).is_valid()
		n_data = self.storage.get_step_data('14')
		n_valid = self.get_form(step='14', data=n_data).is_valid()
		o_data = self.storage.get_step_data('15')
		o_valid = self.get_form(step='15', data=o_data).is_valid()
		p_data = self.storage.get_step_data('16')
		p_valid = self.get_form(step='16', data=p_data).is_valid()
		q_data = self.storage.get_step_data('17')
		q_valid = self.get_form(step='17', data=q_data).is_valid()
		r_data = self.storage.get_step_data('18')
		r_valid = self.get_form(step='18', data=r_data).is_valid()
		s_data = self.storage.get_step_data('19')
		s_valid = self.get_form(step='19', data=s_data).is_valid()
		t_data = self.storage.get_step_data('20')
		t_valid = self.get_form(step='20', data=t_data).is_valid()
		u_data = self.storage.get_step_data('21')
		u_valid = self.get_form(step='21', data=u_data).is_valid()
		v_data = self.storage.get_step_data('22')
		v_valid = self.get_form(step='22', data=v_data).is_valid()
		
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
			a = self.get_form(step='1', data=a_data).save()
			b = self.get_form(step='2', data=b_data).save()
			c = self.get_form(step='3', data=c_data).save()
			d = self.get_form(step='4', data=d_data).save()
			e = self.get_form(step='5', data=e_data).save()
			f = self.get_form(step='6', data=f_data).save()
			g = self.get_form(step='7', data=g_data).save()
			h = self.get_form(step='8', data=h_data).save()
			i = self.get_form(step='9', data=i_data).save()
			j = self.get_form(step='10', data=j_data).save()
			k = self.get_form(step='11', data=k_data).save()
			l = self.get_form(step='12', data=l_data).save()
			m = self.get_form(step='13', data=m_data).save()
			n = self.get_form(step='14', data=n_data).save()
			o = self.get_form(step='15', data=o_data).save()
			p = self.get_form(step='16', data=p_data).save()
			q = self.get_form(step='17', data=q_data).save()
			r = self.get_form(step='18', data=r_data).save(commit=False)
			s = self.get_form(step='19', data=s_data).save()
			t = self.get_form(step='20', data=t_data).save()
			u = self.get_form(step='21', data=u_data).save()
			v = self.get_form(step='22', data=v_data).save()
			
			# Sets BorrowerInfo.user = currently logged in user
			r.user = self.request.user
			r.save()
			
			# Sends email when data is submitted to DB
			send_mail(
				'A Tier 2 application has been submitted', # subject line - will change to add more info
				'This is where the application details will go', # message - will add more info to this
				'noreply@tlc.com', # 'from' email address
				['loanofficer@tlc.com'] # recipient email address
			)
			
		return render(self.request, 'pages/loan_apply_done.html')