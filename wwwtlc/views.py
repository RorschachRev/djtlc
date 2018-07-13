from django import forms
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect

import decimal as D
from .models_loan_app import ApplicationSummary

from wwwtlc.models import Person, Wallet
from wwwtlc.ethereum import BC
from wwwtlc.forms import *

from loan.models import Loan, Loan_Data, Loan_Request
from loan.forms import PersonEditForm, PersonForm, OfficerLoanRequestForm

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
	user = request.user
	if user.is_staff:
		return render(request, 'dashboard/home.html', {})
	else:
		return render(request, 'pages/home.html')
	
def loan(request):
	loan_iterable = Loan.objects.all().filter(user=request.user)
	blockdata=BC()
	applied_loans = Loan_Request.objects.all().filter(user=request.user)
	return render(request, 'pages/loan.html', {'loan_iterable': loan_iterable, 'blockdata': blockdata, 'applied_loans': applied_loans})
	
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
	
def signup(request):
	if request.method == 'POST':
		form = UserCreationForm(request.POST)
		if form.is_valid():
			form.save()
			username = form.cleaned_data.get('username')
			raw_password = form.cleaned_data.get('password1')
			user = authenticate(username=username, password=raw_password)
			login(request, user)
			return redirect('home')
	else:
		form = UserCreationForm()
	return render(request, 'base.html', {'form': form})
	
# Views for Loan Officer Dashboard - currently just template rendering, no data handling
def loan_requests(request):
	loan_requests = Loan_Request.objects.all().order_by('-loan_request_date')
	
	try:
		if request.method == 'POST':
			loanid=0
			print(dir(request.POST.update))
			print('###' + str(request.POST))
			for key in request.POST:
				if key.startswith('loan_'):
					loanid=int(key[5:])	
			app = Loan_Request.objects.get(user=loanid)
			
			form = OfficerLoanRequestForm(request.POST, instance=app)
			if form.is_valid():
				form.save()
			
		app = Loan_Request.objects.all()	
		form = OfficerLoanRequestForm(instance=app)
	except:
		form = OfficerLoanRequestForm()
	return render(request, 'dashboard/loan_request.html', {'requests': loan_requests, 'form': form})
	
def workflow(request):
	return render(request, 'dashboard/workflow.html', {})
	
def workflow_detail(request, app_id):
	loan_request = ApplicationSummary.objects.get(pk=app_id)
	return render(request, 'dashboard/workflow_detail.html', {'app': loan_request})
	
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
		aps = ApplicationSummary
		
		# a, 1 = Address
		# b, 2 = BusinessInfo
		# c, 3 = ConstructionInfo
		# d, 4 = RefinanceInfo
		# e, 5 = PropertyInfo
		# f, 6 = BorrowerInfo
		# g, 7 = CreditRequest
		# h, 8 = Declaration
		# i, 9 = TransactionDetails
		# j, 10 = AcknowledgeAgree
		
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
		
		if (
			a_valid and b_valid and c_valid
			and d_valid and e_valid and f_valid
			and g_valid and h_valid and i_valid
			and j_valid
		):
			a = self.get_form(step='1', data=a_data).save()
			b = self.get_form(step='2', data=b_data).save()
			c = self.get_form(step='3', data=c_data).save()
			d = self.get_form(step='4', data=d_data).save()
			e = self.get_form(step='5', data=e_data).save(commit=False)
			f = self.get_form(step='6', data=f_data).save(commit=False)
			g = self.get_form(step='7', data=g_data).save(commit=False)
			h = self.get_form(step='8', data=h_data).save()
			i = self.get_form(step='9', data=i_data).save()
			j = self.get_form(step='10', data=j_data).save() # will need to add 'commit=False' when AcknowledgeAgree FK's get set automatically
			
			# Sets Address, ConstructionInfo, and RefinanceInfo to PropertyInfo
			e.address = a
			e.construction_loan = c
			e.refinance_loan = d
			e.save()
			
			# Sets User, BusinessInfo, and Declarations to BorrowerInfo
			f.user = self.request.user
			f.business = b
			f.declarations = h
			f.save()
			
			# Populates and saves the ApplicationSummary table
			app_sum = aps(
				user = self.request.user,
				property = e,
				borrower = f, 
				# coborrower = ??? <- coborrower is a FK onto borrowerinfo, will need to figure this out eventually
				acknowledge = j,
			)
			
			app_sum.save()
			
			# Sets Borrower and Application to CreditRequest
			g.borrower = f
			g.application = app_sum
			g.save()
			
			# Will set Borrower and Coborrower fields automatically to AcknowledgeAgree
			# currently unsure of how to separate the two, however. Will need more work
			'''
			j.borrower = f
			j.coborrower = f
			j.save()
			'''
			
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
		aps = ApplicationSummary
		
		# a, 1 = Address
		# b, 2 = BusinessInfo
		# c, 3 = ConstructionInfo
		# d, 4 = RefinanceInfo
		# e, 5 = PropertyInfo
		# f, 6 = EmploymentIncomeInfo
		# g, 7 = BankAccount
		# h, 8 = Bond
		# i, 9 = Stock
		# j, 10 = Vehicle
		# k, 11 = Asset Summary
		# l, 12 = Debt
		# m, 13 = ManagedProperty
		# n, 14 = Alimony
		# o, 15 = ChildSupport
		# p, 16 = SeperateMaintenance
		# q, 17 = LiabilitySummary
		# r, 18 = ALSummary
		# s, 19 = BorrowerInformation
		# t, 20 = CreditRequest
		# u, 21 = Declaration
		# v, 22 = TransactionDetails
		# w, 23 = AcknowledgeAgree
		
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
		w_data = self.storage.get_step_data('23')
		w_valid = self.get_form(step='23', data=w_data).is_valid()
		
		if (
			a_valid and b_valid and c_valid 
			and d_valid and e_valid and f_valid
			and g_valid and h_valid and i_valid
			and j_valid and k_valid and l_valid
			and m_valid and n_valid and o_valid
			and p_valid and q_valid and r_valid
			and s_valid and t_valid and u_valid
			and v_valid and w_valid
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
			j = self.get_form(step='10', data=j_data).save()
			k = self.get_form(step='11', data=k_data).save(commit=False)
			l = self.get_form(step='12', data=l_data).save()
			m = self.get_form(step='13', data=m_data).save()
			n = self.get_form(step='14', data=n_data).save()
			o = self.get_form(step='15', data=o_data).save()
			p = self.get_form(step='16', data=p_data).save()
			q = self.get_form(step='17', data=q_data).save(commit=False)
			r = self.get_form(step='18', data=r_data).save(commit=False)
			s = self.get_form(step='19', data=s_data).save(commit=False)
			t = self.get_form(step='20', data=t_data).save(commit=False)
			u = self.get_form(step='21', data=u_data).save()
			v = self.get_form(step='22', data=v_data).save()
			w = self.get_form(step='23', data=w_data).save()
			
			# Sets Address, ConstructionInfo, and RefinanceInfo to PropertyInfo
			e.address = a
			e.construction_loan = c
			e.refinance_loan = d
			e.save()
			
			# Sets Account1, Stock1, Bond1, Vehicle1, and EmploymentIncome to AssetSummary
			# will eventually look into how to get the form to submit multiple entries for
			# Accounts, Stocks, Bonds, and Vehicles (as well as EmploymentIncome *possibly*)
			# This will need edited later
			k.acct1 = g
			k.stock1 = i
			k.bond1 = h
			k.vehicle1 = j
			k.employment_income = f
			k.save()
			
			# Sets Debt1, Alimony1, ChildSupport1, and SeparateMaint1 to LiabilitySummary
			# will eventually look into how to get the form to submit multiple entries for
			# Debt, Alimony, ChildSupport, and SeparateMaint
			# This will need edited later
			q.debt1 = l
			q.alimony1 = n
			q.child_supp1 = o
			q.separate_maint1 = p
			q.save()
			
			# Sets AssetSummary and LiabilitySummary to ALSummary
			r.assets = k
			r.liabilities = q
			r.save()
			
			# Sets User, BusinessInfo, and Declarations to BorrowerInfo
			s.user = self.request.user
			s.business = b
			s.declarations = u
			s.save()
			
			# Populates and saves the ApplicationSummary table
			app_sum = aps(
				user = self.request.user,
				property = e,
				borrower = s, 
				# coborrower = ??? <- coborrower is a FK onto borrowerinfo, will need to figure this out eventually
				acknowledge = w,
			)
			
			app_sum.save()
			
			# Sets Borrower and Application to CreditRequest
			t.borrower = s
			t.application = app_sum
			t.save()
			
			# Will set Borrower and Coborrower fields automatically to AcknowledgeAgree
			# currently unsure of how to separate the two, however. Will need more work
			'''
			w.borrower = f
			w.coborrower = f
			w.save()
			'''
			
			# Sends email when data is submitted to DB
			send_mail(
				'A Tier 2 application has been submitted', # subject line - will change to add more info
				'This is where the application details will go', # message - will add more info to this
				'noreply@tlc.com', # 'from' email address
				['loanofficer@tlc.com'] # recipient email address
			)
			
		return render(self.request, 'pages/loan_apply_done.html')