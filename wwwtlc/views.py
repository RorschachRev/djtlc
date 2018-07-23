from django import forms
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect

import decimal as D
from wwwtlc.models_officer import ApplicationSummary, NewLoan

from wwwtlc.models_meta import Person, Wallet
from wwwtlc.models_loan_apply import NewRequestSummary
from wwwtlc.ethereum import BC
from wwwtlc.forms import *

from loan.models import Loan_Data, Loan_Request#, Loan
from loan.forms import PersonEditForm, PersonForm, ChangeReqForm

from formtools.wizard.views import NamedUrlSessionWizardView, SessionWizardView


'''##################################################
# Basic Functionality Views	
##################################################'''	
def home(request):
	user = request.user
	if user.is_staff:
		return render(request, 'dashboard/home.html', {})
	else:
		return render(request, 'pages/home.html')
		
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
	
def test(request):
	return render(request, 'pages/test.html')
	
	
'''##################################################
# User Views - mostly unused in current state
##################################################'''
def loan(request):
	loan_iterable = NewLoan.objects.filter(user=request.user)
	blockdata=BC()
	req_tier1 = NewRequestSummary.objects.filter(user=request.user, status=3).order_by('-submitted')
	req_tier2 = NewRequestSummary.objects.filter(user=request.user, status=4).order_by('-submitted')
	applied_loans = NewRequestSummary.objects.filter(status__in=[0, 1, 2], user=request.user).order_by('-status', '-submitted')
	return render(request, 'pages/loan.html', {'loan_iterable': loan_iterable, 'blockdata': blockdata, 'applied_loans': applied_loans, 'req_tier1': req_tier1, 'req_tier2': req_tier2})
	
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
	loaninfo.wallet_addr= str(NewLoan.objects.get(pk=loan_id).loan_wallet.address)
	blockdata=BC()
	blockdata.loanbal=blockdata.get_loan_bal(loaninfo.wallet_addr) / 100
	loaninfo.payment=NewLoan.objects.get(pk=loan_id).payment_due
	blockdata.tlctousdc=D.Decimal(blockdata.get_TLC_USDc() ) / 100000000 
	loaninfo.payTLC= loaninfo.payment / blockdata.tlctousdc
	return render(request, 'pages/pay.html', {'loan': loaninfo, 'blockdata':blockdata} )
	
'''##################################################
# Loan Officer/Dashboard Views
##################################################'''
# REQUESTS / WORKFLOW
##################

def loan_requests(request):
	sleep_requests = NewRequestSummary.objects.filter(status=0).order_by('-submitted')
	active_requests = NewRequestSummary.objects.filter(status=1).order_by('-submitted')
	priority_requests = NewRequestSummary.objects.filter(status=2).order_by('-submitted')
	if request.method == 'GET':
		sleep_vis = request.GET.get('sleep_vis')
		if sleep_vis == '0':
			sleep_vis = False
		elif sleep_vis == '1':
			sleep_vis = True
	return render(request, 'dashboard/loan_request.html', {'active': active_requests, 'sleep': sleep_requests, 'priority': priority_requests, 'sleep_vis': sleep_vis})
	
def change_reqstatus(request, app_id):
	app = NewRequestSummary.objects.get(pk=app_id)
	
	try:
		if request.method == 'POST':
			form = ChangeReqForm(request.POST, instance=app)
			if form.is_valid():
				form.save()
				return HttpResponseRedirect('/loan_requests')
		else:
			form = ChangeReqForm(instance=app)
	except:
		form = ChangeReqForm()
	return render(request, 'dashboard/change_reqstatus.html', {'app': app, 'form': form})
	
	
def workflow(request):
	req_tier1 = NewRequestSummary.objects.filter(status=3).order_by('-submitted')
	req_tier2 = NewRequestSummary.objects.filter(status=4).order_by('-submitted')
	tier1 = ApplicationSummary.objects.filter(tier=0).exclude(status=12).order_by('-submission_date')
	tier2 = ApplicationSummary.objects.filter(tier=1).exclude(status=12).order_by('-submission_date')
	cert_tier1 = ApplicationSummary.objects.filter(status=12, tier=0).order_by('-submission_date')
	cert_tier2 = ApplicationSummary.objects.filter(status=12, tier=1).order_by('-submission_date')
	return render(request, 'dashboard/workflow.html', {'tier1': tier1, 'tier2': tier2, 'req_tier1': req_tier1, 'req_tier2': req_tier2, 'cert_tier1': cert_tier1, 'cert_tier2': cert_tier2})
	
# This function handles all possible requests on the '/workflow' page
# handling for this comes from passing data via url into the view,
# hence the "if app_id[:4] == 'foo_':"
def workflow_request(request, app_id):
	if app_id[:4] == 'req_':
		app = app_id[4:]
		app = NewRequestSummary.objects.get(pk=app)
		
		try:
			if request.method == 'POST':
				form = ChangeReqForm(request.POST, instance=app)
				if form.is_valid():
					form.save()
					return HttpResponseRedirect('/workflow')
			else:
				form = ChangeReqForm(instance=app)
				return render(request, 'dashboard/wf_request.html', {'app': app, 'form': form})
		except:
			form = ChangeReqForm()
			return render(request, 'dashboard/wf_request.html', {'app': app, 'form': form})
			
	elif app_id[:4] == 'cht_':
		app = app_id[4:]
		app = ApplicationSummary.objects.get(pk=app)
		
		try:
			if request.method == 'POST':
				form = AppTierForm(request.POST, instance=app)
				if form.is_valid():
					form.save()
					return HttpResponseRedirect('/workflow')
			else:
				form = AppTierForm(instance=app)
				return render(request, 'dashboard/workflow_update.html', {'app': app, 'form': form})
		except:
			form = AppTierForm()
			return render(request, 'dashboard/workflow_update.html', {'app': app, 'form': form})
	elif app_id[:4] == 'chs_':
		app = app_id[4:]
		app = ApplicationSummary.objects.get(pk=app)
		
		try:
			if request.method == 'POST':
				form = AppStatusForm(request.POST, instance=app)
				if form.is_valid():
					form.save()
					return HttpResponseRedirect('/workflow')
			else:
				form = AppStatusForm(instance=app)
				return render(request, 'dashboard/workflow_update.html', {'app': app, 'form':form})
		except:
			form = AppStatusForm()
			return render(request, 'dashboard/workflow_update.html', {'app': app, 'form': form})
	else:
		loan_request = ApplicationSummary.objects.get(pk=app_id)
		credit_request = CreditRequest.objects.get(application=app_id)
		return render(request, 'dashboard/workflow_detail.html', {'app': loan_request, 'credit': credit_request})
		
def certify(request, app_id='0'):
	tier1 = ApplicationSummary.objects.filter(tier=0).order_by('-submission_date')
	tier2 = ApplicationSummary.objects.filter(tier=1).order_by('-submission_date')
	
	if app_id[:3] != 0 and app_id[:3] == 't1_':
		#app = ApplicationSummary.objects.get(pk=app_id[3:])
		app = ApplicationSummary.objects.filter(application=app_id[3:])
		return render(request, 'dashboard/sources.html', {'app': app})
		
	elif app_id[:3] != 0 and app_id[:3] == 't1e':
		app = ApplicationSummary.objects.get(application=app_id[3:])
		
		if request.method == 'POST':
			form = ApplicationSummaryForm(request.POST, instance=app)
			if form.is_valid():
				form.save()
				return HttpResponseRedirect('/certify')
		else:
			form = ApplicationSummaryForm(instance=app)
			return render(request, 'dashboard/edit_summary.html', {'form': form})
			
	return render(request, 'dashboard/certify.html', {'tier1': tier1, 'tier2': tier2})
	
# PAYMENTS / ACCOUNTING
###################

# currently allows for user to select both wallet and loan id, 
# which will need to change to minimize human error
# (ie. picking wrong wallet for loan)
def make_payment(request, loan_id):
	loan = NewLoan.objects.get(pk=loan_id)
	
	if request.method == 'POST':
		form = PaymentForm(request.POST)
		if form.is_valid():
			obj = form.save(commit=False)
			obj.wallet = loan.loan_wallet
			obj.loan = loan
			obj.save()
			return HttpResponseRedirect('/loan_payments')
	else:
		form = PaymentForm()
	return render(request, 'dashboard/make_payment.html', {'loan':loan, 'form':form})
	
def loan_payments(request):
	loan_iterable = NewLoan.objects.all()
	return render(request, 'dashboard/loan_payments.html', {'loan_iterable': loan_iterable})
	
def payment_history(request):
	history_iterable = LoanPaymentHistory.objects.all().order_by('-pmt_date')
	return render(request, 'dashboard/payment_history.html', {'payments': history_iterable})
	
def loan_accounting(request):
	return render(request, 'dashboard/loan_accounting.html', {})
	
def credit_verify(request):
	return render(request, 'dashboard/credit_verify.html', {})
	
def submit_loan(request):
	form = LoanForm
	return render(request, 'dashboard/submit_loan.html', {'form': form})
	
def manage_loan(request):
	return render(request, 'dashboard/manage_loan.html', {})
	
	
'''##################################################
# Form Views
##################################################'''
# Form for Loan Apply
class LoanApplyWizard(SessionWizardView):
	def done(self, form_list, **kwargs):
		summary = NewRequestSummary
		
		# a, 0 = AddressForm
		# b, 1 = ContactRequestForm
		# c, 2 = PropertyInfoRequestForm
		# d, 3 = CurrentMortgageForm
		# e, 4 = MortgageDesiredForm
		# f, 5 = BorrowerInfoRequestForm
		
		# This block of code binds data from form to form itself, and validates the data
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
		
		# This block of code sets the foreign keys of each table to the entries entered in the previous form step, if the data is valid
		if (
			a_valid and b_valid and c_valid and
			d_valid and e_valid and f_valid
		):
			a = self.get_form(step='0', data=a_data).save()
			b = self.get_form(step='1', data=b_data).save()
			c = self.get_form(step='2', data=c_data).save(commit=False)
			d = self.get_form(step='3', data=d_data).save()
			e = self.get_form(step='4', data=e_data).save()
			f = self.get_form(step='5', data=f_data).save()
			
			c.property_address = a
			c.save()
			
			summary = summary(
				user = self.request.user,
				contact = b,
				property = c,
				curr_mortgage = d,
				desired_mortgage = e,
				borrower = f,
			)
			
			summary.save()
			
			# sends email when data is submitted and validated
			send_mail(
				# subject line - returns LoanData __str__ method
				'New Loan Request',
				
				# message
				'A new loan request has been submitted and can be found in the officer dashboard.', 
				
				# 'from' email address
				'no_reply@thelendingcoin.com',
				
				# recipient email address
				['finance@thelendingcoin.com', 'lender@thelendingcoin.com']
			)
			
		return render(self.request, 'pages/loan_apply_done.html', {'name': b.name_first + ' ' + b.name_last} )
		
# Django FormWizard view for Basic Application
class BasicWizard(NamedUrlSessionWizardView):
	def done(self, form_list, **kwargs):
		aps = ApplicationSummary
		
		# a, 1 = Address
		# b, 2 = BusinessInfo
		# c, 3 = ConstructionInfo
		# e, 4 = PropertyInfo
		# f, 5 = BorrowerInfo
		# g, 6 = CreditRequest
		# h, 7 = Declaration
		# i, 8 = AcknowledgeAgree
		
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
		
		if (
			a_valid and b_valid and c_valid
			and d_valid and e_valid and f_valid
			and g_valid and h_valid
		):
			a = self.get_form(step='1', data=a_data).save()
			b = self.get_form(step='2', data=b_data).save()
			c = self.get_form(step='3', data=c_data).save()
			d = self.get_form(step='4', data=d_data).save()
			e = self.get_form(step='5', data=e_data).save()
			f = self.get_form(step='6', data=f_data).save()
			g = self.get_form(step='7', data=g_data).save()
			h = self.get_form(step='8', data=h_data).save() # will need to add 'commit=False' when AcknowledgeAgree FK's get set automatically
			
			# will need to change drastically
			'''# Sets Address, ConstructionInfo, and RefinanceInfo to PropertyInfo
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
				tier = 0,
			)
			
			app_sum.save()
			
			# Sets Borrower and Application to CreditRequest
			g.borrower = f
			g.application = app_sum
			g.save()
			
			# Will set Borrower and Coborrower fields automatically to AcknowledgeAgree
			# currently unsure of how to separate the two, however. Will need more work
			i.borrower = f
			i.coborrower = f
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
		
# Form for Standard application
class StandardWizard(NamedUrlSessionWizardView):
	def done(self, form_list, **kwargs):
		aps = ApplicationSummary
		
		# a, 1 = Address
		# b, 2 = BusinessInfo
		# c, 3 = ConstructionInfo
		# d, 4 = PropertyInfo
		# e, 5 = EmploymentIncomeInfo
		# f, 6 = BankAccount
		# g, 7 = Asset Summary
		# h, 8 = ManagedProperty
		
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
		
		if (
			a_valid and b_valid and c_valid 
			and d_valid and e_valid and f_valid
			and g_valid and h_valid
		):
			a = self.get_form(step='1', data=a_data).save()
			b = self.get_form(step='2', data=b_data).save()
			c = self.get_form(step='3', data=c_data).save()
			d = self.get_form(step='4', data=d_data).save()
			e = self.get_form(step='5', data=e_data).save()
			f = self.get_form(step='6', data=f_data).save()
			g = self.get_form(step='7', data=g_data).save()
			h = self.get_form(step='8', data=h_data).save()
			
			# will need to change drastically
			'''# Sets Address, ConstructionInfo, and RefinanceInfo to PropertyInfo
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
				tier = 1
			)
			
			app_sum.save()
			
			# Sets Borrower and Application to CreditRequest
			t.borrower = s
			t.application = app_sum
			t.save()
			
			# Will set Borrower and Coborrower fields automatically to AcknowledgeAgree
			# currently unsure of how to separate the two, however. Will need more work
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
		
# Form to Create a Loan
# will probably remove or at the very least update
class LoanWizard(SessionWizardView):
	def done(self, form_list, **kwargs):
		# a, 0 = BorrowerInfo
		# b, 1 = LoanTerms
		# c, 2 = Loan Wallet
		# d, 3 = NewLoan
		
		a_data = self.storage.get_step_data('0')
		a_valid = self.get_form(step='0', data=a_data).is_valid()
		b_data = self.storage.get_step_data('1')
		b_valid = self.get_form(step='1', data=b_data).is_valid()
		c_data = self.storage.get_step_data('2')
		c_valid = self.get_form(step='2', data=c_data).is_valid()
		d_data = self.storage.get_step_data('3')
		d_valid = self.get_form(step='3', data=d_data).is_valid()
		
		if (
			a_valid and b_valid and
			c_valid and d_valid
		):
			a = self.get_form(step='0', data=a_data).save()
			b = self.get_form(step='1', data=b_data).save()
			c = self.get_form(step='2', data=c_data).save(commit=False)
			d = self.get_form(step='3', data=d_data).save(commit=False)
			
			c.wallet = a.user
			c.save()
			
			d.user = a.user
			d.borrower = a
			d.loan_terms = b
			d.loan_wallet = c
			
			d.save()
			
		return HttpResponseRedirect('/loan_payments')
		
# from old views_form.py
# unsure if these are necessary
'''
from django import forms
from django.conf import settings
from django.shortcuts import render, get_object_or_404
from django.core.mail import send_mail

def account(request):
	return render(request, 'pages/account.html')
	
def wallet(request):
	return render(request, 'pages/wallet.html')	
'''