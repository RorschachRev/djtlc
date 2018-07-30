from django import forms
from django.conf import settings
from django.core import serializers
from django.utils.html import escape
from django.http import JsonResponse
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect, HttpResponse, render_to_response

import decimal as D
from wwwtlc.forms import *
from wwwtlc.ethereum import BC
from wwwtlc.models_officer import NewLoan
from wwwtlc.models_meta import Person, Wallet
from wwwtlc.models_bse import ApplicationSummary
from wwwtlc.models_loan_apply import NewRequestSummary

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
			obj = form.save(commit=False)
			x = User.objects.values('id')
			z = []
			for y in x:
				for k, v in y.items():
					z.append(v)
			max_id = max(z)
			if max_id > 1024:
				obj.id = max_id + 1
			else:
				obj.id = 1025
			obj.save()
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
	req_basic = NewRequestSummary.objects.filter(user=request.user, status=3).order_by('-submitted')
	req_standard = NewRequestSummary.objects.filter(user=request.user, status=4).order_by('-submitted')
	applied_loans = NewRequestSummary.objects.filter(status__in=[0, 1, 2], user=request.user).order_by('-status', '-submitted')
	return render(request, 'pages/loan.html', {'loan_iterable': loan_iterable, 'blockdata': blockdata, 'applied_loans': applied_loans, 'req_basic': req_basic, 'req_standard': req_standard})
	
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

	payments = LoanPaymentHistory.objects.filter(loan__user=request.user).order_by('-pmt_date')
	return render(request, 'pages/payhistory.html', {'loan': loaninfo, 'blockdata':blockdata, 'payments': payments })
	
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
	
# this function selects a specific loan associated with the user and displays just that one,
# may not work as intended anymore. 
def pay(request, loan_id, principal_paid=0):
	loaninfo.wallet_addr= str(NewLoan.objects.get(pk=loan_id).loan_wallet.address)
	blockdata=BC()
	blockdata.loanbal=blockdata.get_loan_bal(loaninfo.wallet_addr) / 100
	loaninfo.payment=principal_paid
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
	req_basic = NewRequestSummary.objects.filter(status=3).order_by('-submitted')
	req_standard = NewRequestSummary.objects.filter(status=4).order_by('-submitted')
	basic = ApplicationSummary.objects.filter(tier=0).exclude(status=12).order_by('-submission_date')
	standard = ApplicationSummary.objects.filter(tier=1).exclude(status=12).order_by('-submission_date')
	cert_basic = ApplicationSummary.objects.filter(status=12, tier=0).order_by('-submission_date')
	cert_standard = ApplicationSummary.objects.filter(status=12, tier=1).order_by('-submission_date')
	return render(request, 'dashboard/workflow.html', {'basic': basic, 'standard': standard, 'req_basic': req_basic, 'req_standard': req_standard, 'cert_basic': cert_basic, 'cert_standard': cert_standard})
	
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
		credit_request = CreditRequest.objects.get(application=loan_request)
		return render(request, 'dashboard/workflow_detail.html', {'app': loan_request, 'credit': credit_request})
		
# Incomplete, will need work later		
def certify(request, app_id='0'):
	basic = ApplicationSummary.objects.filter(tier=0).order_by('-submission_date')
	standard = ApplicationSummary.objects.filter(tier=1).order_by('-submission_date')
	
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
			
	return render(request, 'dashboard/certify.html', {'basic': basic, 'standard': standard})
	
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
			
			loan.interest_paid += obj.interest_pmt
			loan.principal_paid += obj.principal_pmt
			loan.principal_balance -= obj.principal_pmt
			loan.payments_left -= 1
			loan.save()
			submit = pay(request, loan_id=obj.loan.id, principal_paid=obj.principal_pmt)
			return submit
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
	loan_iterable = NewLoan.objects.all()
	return render(request, 'dashboard/manage_loan.html', {'loan_iterable': loan_iterable})

def loan_details(request, loan_id):
	loan = NewLoan.objects.get(pk=loan_id)
	return render(request, 'dashboard/loan_details.html', {'loan': loan})
	
	
'''##################################################
# Form Views
##################################################'''
def handle_pop_add(request, addForm, field):
	if request.method == "POST":
		form = addForm(request.POST)
		if form.is_valid():
			try:
				newObject = form.save(commit=False)
				newObject.user = request.user
				newObject.source = request.user
				newObject.save()
			except (forms.ValidationError):
				newObject = None
			if newObject:
				return HttpResponse('<script type="text/javascript">opener.dismissAddAnotherPopup(window, "%s", "%s");</script>' % \
			(escape(newObject._get_pk_val()), escape(newObject)))
	else:
		form = addForm()
		
	pageContext = {'form': form, 'field': field}
	return render(request, "form/add_new.html", pageContext)
	
def new_field(request, field_name):
	if 'address' in field_name:
		new_field=field_name
		return handle_pop_add(request, AddressForm, new_field)
	elif 'borrower' in field_name:
		new_field=field_name
		return handle_pop_add(request, BorrowerInfoForm, new_field)

# Form for Loan Apply
class LoanApplyWizard(SessionWizardView):
	# Function to send the form some initial values
	def get_form_initial(self, step):
		user = self.request.user
		if step == '1':
			self.initial_dict = {'user': user}
		return self.initial_dict
	
	def done(self, form_list, **kwargs):
		summary = NewRequestSummary
		
		# a, 0 = ContactRequestForm
		# b, 1 = PropertyInfoRequestForm
		# c, 2 = CurrentMortgageForm
		# d, 3 = MortgageDesiredForm
		# e, 4 = BorrowerInfoRequestForm
		
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
		
		# This block of code sets the foreign keys of each table to the entries entered in the previous form step, if the data is valid
		if (
			a_valid and b_valid and c_valid and
			d_valid and e_valid
		):
			a = self.get_form(step='0', data=a_data).save(commit=False)
			b = self.get_form(step='1', data=b_data).save(commit=False)
			c = self.get_form(step='2', data=c_data).save(commit=False)
			d = self.get_form(step='3', data=d_data).save(commit=False)
			e = self.get_form(step='4', data=e_data).save(commit=False)
			
			a.source = self.request.user
			a.save()
			
			b.source = self.request.user
			b.save()
			
			c.source = self.request.user
			c.save()
			
			d.source = self.request.user
			d.save()
			
			e.source = self.request.user
			e.save()
			
			summary = summary(
				user = self.request.user,
				source = self.request.user,
				contact = a,
				property = b,
				curr_mortgage = c,
				desired_mortgage = d,
				borrower = e,
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
			
		return render(self.request, 'pages/loan_apply_done.html', {'name': a.name_first + ' ' + a.name_last} )
		
# Django FormWizard view for Basic Application
class BasicWizard(NamedUrlSessionWizardView):
	# Function to send the form some initial values
	def get_form_initial(self, step):
		user = self.request.user
		if step == '3' or step == '4':
			self.initial_dict = {'user': user}
		return self.initial_dict
	
	def done(self, form_list, **kwargs):
		aps = ApplicationSummary
		
		# a, 1 = BusinessInfo
		# b, 2 = ConstructionInfo
		# c, 3 = PropertyInfo
		# d, 4 = BorrowerInfo
		# e, 5 = CreditRequest
		# f, 6 = Declaration
		# g, 7 = AcknowledgeAgree
		
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
		
		if (
			a_valid and b_valid and c_valid and 
			d_valid and e_valid and f_valid and 
			g_valid
		):
			a = self.get_form(step='1', data=a_data).save(commit=False)
			b = self.get_form(step='2', data=b_data).save(commit=False)
			c = self.get_form(step='3', data=c_data).save(commit=False)
			d = self.get_form(step='4', data=d_data).save(commit=False)
			e = self.get_form(step='5', data=e_data).save(commit=False)
			f = self.get_form(step='6', data=f_data).save(commit=False)
			g = self.get_form(step='7', data=g_data).save(commit=False) # will need to add 'commit=False' when AcknowledgeAgree FK's get set automatically
			
			a.source = self.request.user
			a.save()
			
			b.source = self.request.user
			b.save()
			
			# Saves Foreign Keys for 'PropertyInfoForm'
			c.source = self.request.user
			c.construction_loan = b
			c.save()
			
			f.source = self.request.user
			f.save()
			
			# Saves Foreign Keys for 'BorrowerInfoForm'
			d.user = self.request.user
			d.source = self.request.user
			d.business = a
			d.declarations = f
			d.save()
			
			g.source = self.request.user
			g.save()
			
			# Creates 'ApplicationSummary' off of step data
			summary = aps(
				user = self.request.user,
				source = self.request.user,
				property = c,
				borrower = d,
				acknowledge = g,
				tier = 0,
			)
			summary.save()
			
			# Saves Foreign Keys for 'CreditRequestForm'
			e.source = self.request.user
			e.borrower = d
			e.application = summary
			e.save()
			
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
	# Function to send the form some initial values
	def get_form_initial(self, step):
		user = self.request.user
		if step == '3' or step == '4' or step == '10':
			self.initial_dict = {'user': user}
		return self.initial_dict
		
	def done(self, form_list, **kwargs):
		aps = ApplicationSummary
		
		# a, 1 = BusinessInfo
		# b, 2 = ConstructionInfo
		# c, 3 = PropertyInfo
		# d, 4 = EmploymentIncomeInfo
		# e, 5 = BankAccount
		# f, 6 = Asset Summary
		# g, 7 = ManagedProperty
		# h, 8 = CreditRequest
		# i, 9 = Declarations
		# j, 10 = BorrowerInfo
		# k, 11 = AcknowledgeAgree
		
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
		
		if (
			a_valid and b_valid and c_valid and
			d_valid and e_valid and f_valid and 
			g_valid and h_valid and i_valid and
			j_valid and k_valid
		):
			a = self.get_form(step='1', data=a_data).save(commit=False)
			b = self.get_form(step='2', data=b_data).save(commit=False)
			c = self.get_form(step='3', data=c_data).save(commit=False)
			d = self.get_form(step='4', data=d_data).save(commit=False)
			e = self.get_form(step='5', data=e_data).save(commit=False)
			f = self.get_form(step='6', data=f_data).save(commit=False)
			g = self.get_form(step='7', data=g_data).save(commit=False)
			h = self.get_form(step='8', data=h_data).save(commit=False)
			i = self.get_form(step='9', data=i_data).save(commit=False)
			j = self.get_form(step='10', data=j_data).save(commit=False)
			k = self.get_form(step='11', data=k_data).save(commit=False)
			
			a.source = self.request.user
			a.save()
			
			b.source = self.request.user
			b.save()
			
			# Saves Foreign Keys for 'PropertyInfoForm'
			c.source = self.request.user
			c.construction_loan = b
			c.save()
			
			d.source = self.request.user
			d.save()
			
			e.source = self.request.user
			e.save()
			
			# Saves Foreign Keys for 'AssetSummaryForm'
			f.source = self.request.user
			f.acct1 = e
			f.employment_income = d
			f.save()
			
			g.source = self.request.user
			g.save()
			
			i.source = self.request.user
			i.save()
			
			# Saves Foreign Keys for 'BorrowerInfoForm'
			j.user = self.request.user
			j.source = self.request.user
			j.business = a
			j.declarations = i
			j.save()
			
			k.source = self.request.user
			k.save()
			
			# Creates 'ApplicationSummary' off of step data
			# Will not work, need data for borrower
			summary = aps(
				user = self.request.user,
				source = self.request.user,
				property = c,
				borrower = j,
				acknowledge = k,
				tier = 1,
			)
			summary.save()
			
			# Saves Foreign Keys to 'CreditRequestForm'
			h.source = self.request.user
			h.borrower = j
			h.application = summary
			h.save()
			
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