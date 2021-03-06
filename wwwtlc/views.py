from django import forms
from django.conf import settings
from django.core import serializers
from django.utils.html import escape
from django.http import JsonResponse
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.db.models.functions import Extract
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect, HttpResponse, render_to_response, reverse

import os
import web3
import pytz
import json
import datetime
import decimal as D

from wwwtlc import events
from wwwtlc.eth import BC
from wwwtlc.forms import *
from wwwtlc import explorer, audit
from wwwtlc.tx_hashes import rop_tx, main_tx
from wwwtlc.models_officer import NewLoan
from wwwtlc.models_bse import ApplicationSummary
from wwwtlc.named_tlc_functions import functions
from wwwtlc.models_meta import Person, Wallet, Contract
from wwwtlc.models_loan_apply import NewRequestSummary

from loan.models import Loan_Data, Loan_Request#, Loan
from loan.forms import PersonEditForm, PersonForm, ChangeReqForm

from formtools.wizard.views import NamedUrlSessionWizardView, SessionWizardView

from xhtml2pdf import pisa
from pymongo import MongoClient
from web3 import Web3
from django.template import Context
from django.template.loader import get_template

'''##################################################
# Basic Functionality Views	
##################################################'''	
def test(request):
	#Wallet Test
	return render(request, 'pages/testwallet.html')
		
	
def home(request):
	user = request.user
	if user.is_staff:
		return render(request, 'dashboard/home.html', {})
	else:
		return render(request, 'pages/home.html', {})
				
def account(request):
	user = request.user
	try:
		acct_info = Person.objects.get(user=user)
		if request.method == 'POST':
			form = PersonForm(request.POST, instance=acct_info)
			if form.is_valid():
				obj = form.save(commit=False)
				obj.user = user
				obj.save()
		else:
			form = PersonForm(instance=acct_info)
	except:
		form = PersonForm()
		if request.method == 'POST':
			form = PersonForm(request.POST)
			if form.is_valid():
				obj = form.save(commit=False)
				obj.user = user
				obj.save()
		else:
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
	return render(request, 'pages/signup.html', {'form': form})

	
'''##################################################
# User Views
##################################################'''
def loan(request):
	loan_iterable = NewLoan.objects.filter(user=request.user)
	blockdata=BC()
	#basic = ApplicationSummary.objects.filter(user=request.user, status=0).order_by('-submission_date')
	standard = ApplicationSummary.objects.filter(user=request.user, status=1).order_by('-submission_date')
	#req_basic = NewRequestSummary.objects.filter(user=request.user, status=3).order_by('-submitted')
	req_standard = NewRequestSummary.objects.filter(user=request.user, status=4).order_by('-submitted')
	applied_loans = NewRequestSummary.objects.filter(status__in=[0, 1, 2], user=request.user).order_by('-status', '-submitted')
	return render(request, 'pages/loan.html', {'loan_iterable': loan_iterable, 'blockdata': blockdata, 'applied_loans': applied_loans, 'req_standard': req_standard, 'standard': standard})#, 'basic': basic, 'req_basic': req_basic})
	
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

def loan_requests(request, app_id='0'):
	sleep_requests = NewRequestSummary.objects.filter(status=0).order_by('-submitted')
	active_requests = NewRequestSummary.objects.filter(status=1).order_by('-submitted')
	priority_requests = NewRequestSummary.objects.filter(status=2).order_by('-submitted')
	if request.method == 'GET':
		sleep_vis = request.GET.get('sleep_vis')
		if sleep_vis == '0':
			sleep_vis = False
		elif sleep_vis == '1':
			sleep_vis = True
			
	if app_id[:4] == 'sta_':
		app = NewRequestSummary.objects.get(pk=app_id[4:])
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
		
	elif app_id[:4] == 'det_':
		app = NewRequestSummary.objects.get(pk=app_id[4:])
		return render(request, 'dashboard/request_details.html', {'app': app})
		
	else:
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
	if request.method == 'GET':
		submit_vis = request.GET.get('submit_vis')
		if submit_vis == '0':
			submit_vis = False
		elif submit_vis == '1':
			submit_vis = True
			
	#req_basic = NewRequestSummary.objects.filter(status=3).order_by('-submitted')
	req_standard = NewRequestSummary.objects.filter(status=4).order_by('-submitted')
	#basic = ApplicationSummary.objects.filter(tier=0).exclude(status=12).order_by('-submission_date')
	standard = ApplicationSummary.objects.filter(tier=1).exclude(status=12).order_by('-submission_date')
	#cert_basic = ApplicationSummary.objects.filter(status=12, tier=0).order_by('-submission_date')
	cert_standard = ApplicationSummary.objects.filter(status=12, tier=1).order_by('-submission_date')
	submitted = NewRequestSummary.objects.filter(status=5).order_by('-submitted')
	return render(request, 'dashboard/workflow.html', {'standard': standard, 'req_standard': req_standard, 'cert_standard': cert_standard, 'submitted': submitted, 'submit_vis': submit_vis})#, 'basic': basic, 'req_basic': req_basic, 'cert_basic': cert_basic})
	
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
	
	elif app_id[:4] == 'det_':
		app = NewRequestSummary.objects.get(pk=app_id[4:])
		return render(request, 'dashboard/request_details.html', {'app': app})
			
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
		
def manage_loan(request, loan_id=0):
	if loan_id == 0:
		loan_iterable = NewLoan.objects.all().order_by('id')
	else:
		loan = NewLoan.objects.get(pk=loan_id)
		return render(request, 'dashboard/loan_details.html', { 'loan': loan })
	return render(request, 'dashboard/manage_loan.html', { 'loans': loan_iterable })
	
def manage_loan_forms(request, loan_id='0'):
	if loan_id[:4] == 'pdd_':
		loan = NewLoan.objects.get(pk=loan_id[4:])
		try:
			if request.method == 'POST':
				form = PaymentDueDateForm(request.POST, instance=loan)
				if form.is_valid():
					form.save()
					return HttpResponseRedirect('/manage_loan')
			else:
				form = PaymentDueDateForm(instance=loan)
				return render(request, 'dashboard/manage_loan_forms.html', {'form': form, 'loan': loan})
		except:
			form = PaymentDueDateForm()
			return render(request, 'dashboard/manage_loan_forms.html', {'form': form, 'loan': loan})
	elif loan_id[:4] == 'pmd_':
		loan = NewLoan.objects.get(pk=loan_id[4:])
		try:
			if request.method == 'POST':
				form = PaymentDueForm(request.POST, instance=loan)
				if form.is_valid():
					form.save()
					return HttpResponseRedirect('/manage_loan')
			else:
				form = PaymentDueForm(instance=loan)
				return render(request, 'dashboard/manage_loan_forms.html', {'form': form, 'loan': loan})
		except:
			form = PaymentDueForm()
			return render(request, 'dashboard/manage_loan_forms.html', {'form': form, 'loan': loan})
	
# PAYMENTS / ACCOUNTING
###################

def submit_loan(request, app_id='0'):
	basic = ApplicationSummary.objects.filter(tier=0).order_by('-submission_date')
	standard = ApplicationSummary.objects.filter(tier=1).order_by('-submission_date')
	converted = ApplicationSummary.objects.filter(tier=2).order_by('-submission_date')
	
	if request.method == 'GET':
		convert_vis = request.GET.get('convert_vis')
		if convert_vis == '0':
			convert_vis = False
		elif convert_vis == '1':
			convert_vis = True
	
	if app_id[:3] != 0 and app_id[:3] == 'c2l':
		app = ApplicationSummary.objects.get(pk=app_id[3:])
		credit = CreditRequest.objects.get(application=app)
		return render(request, 'dashboard/confirm_app_info.html', {'app': app, 'credit': credit})
		
	return render(request, 'dashboard/submit_loan.html', {'basic': basic, 'standard': standard, 'converted': converted, 'convert_vis': convert_vis})

# TODO: write views to handle the BC/Deed logic	
# This view has been commented out due to it not being completed just yet
# The above 'submit_loan' is a hotfix to allow apps to be converted into
# loans on the production server. That hotfix will eventually be replaced
# by the below code.
'''def submit_loan(request, app_id='0'):
	#basic = ApplicationSummary.objects.filter(tier=0).order_by('-submission_date')
	standard = ApplicationSummary.objects.filter(tier=1).order_by('-submission_date')
	converted = ApplicationSummary.objects.filter(tier=2).order_by('-submission_date')
	
	if request.method == 'GET':
		finalized_vis = request.GET.get('finalized_vis')
		if finalized_vis == '0':
			finalized_vis = False
		elif finalized_vis == '1':
			finalized_vis = True
	
	if app_id[:3] != 0 and app_id[:3] == 'c2l':
		app = ApplicationSummary.objects.get(pk=app_id[3:])
		credit = CreditRequest.objects.get(application=app)
		return render(request, 'dashboard/confirm_app_info.html', {'app': app, 'credit': credit})
	# edit loan_terms
	elif app_id[:3] != 0 and app_id[:3] == 'elt':
		loan_terms = LoanTerms.objects.get(application=app_id[3:])
		try:
			if request.method == 'POST':
				form = LoanTermsForm(request.POST, instance=loan_terms)
				if form.is_valid():
					form.save()
					return HttpResponseRedirect('/submit_loan')
			else:
				form = LoanTermsForm(instance=loan_terms)
				return render(request, 'dashboard/submit_forms.html', {'form': form, 'loan_terms': loan_terms})
		except:
			form = LoanTermsForm()
			return render(request, 'dashboard/submit_forms.html', {'form': form, 'loan_terms': loan_terms})
	# edit deed
	elif app_id[:3] != 0 and app_id[:3] == 'edd':
		success = 'edd works'
		return render(request, 'dashboard/submit_forms.html', {'success': success})
	# publish loan_terms
	elif app_id[:3] != 0 and app_id[:3] == 'pbl':
		loan_terms = LoanTerms.objects.get(application=app_id[3:])
		return render(request, 'dashboard/submit_forms.html', {'loan_terms': loan_terms})
	# publish deed
	elif app_id[:3] != 0 and app_id[:3] == 'pbd':
		success = 'pbd works'
		return render(request, 'dashboard/submit_forms.html', {'success': success})
		
	return render(request, 'dashboard/submit_loan.html', {'standard': standard, 'converted': converted, 'finalized_vis': finalized_vis})# 'basic': basic})'''
	
# TODO: Test this view on the blockchain to see if data can be pulled and displayed	
def payment_history(request, loan_id=0):
	if loan_id == 0:
		loans = NewLoan.objects.all().order_by('id')
		return render(request, 'dashboard/payment_history.html', {'loans': loans})
	else:
		loaninfo.wallet_addr= str(NewLoan.objects.get(pk=loan_id).loan_wallet.address)[2:]
		blockdata=BC()
		#Begin Gio's Code
		if loaninfo.wallet_addr[:2] == "0x":
			loaninfo.wallet_addr[2:]
		else:
			loaninfo.wallet_addr="d520f58d25f7259c9a03e4d861a593d7cdfe92df" #hax by ian
		blockdata.loanbal=    blockdata.get_loan_bal(loaninfo.wallet_addr) /100
		blockdata.tlctousdc=  blockdata.get_TLC_USDc()  /100000000
		blockdata.deedloan=  ('https://cloudflare-ipfs.com/ipfs/%s')%(bytearray.fromhex(blockdata.get_deed_loan(loaninfo.wallet_addr)).decode() )
		blockdata.paidfee=    blockdata.get_paid_fee(loaninfo.wallet_addr)
		blockdata.paidinterest=  blockdata.get_paid_interest(loaninfo.wallet_addr) 
		blockdata.paidprincipal= blockdata.get_paid_principal(loaninfo.wallet_addr)
		#blockdata.allowloan=  blockdata.get_allow_loan(loaninfo.wallet_addr)
		blockdata.currentbal= blockdata.get_bal_of(loaninfo.wallet_addr) 
		#End Gio's Code
		#loaninfo.payment=0   #supposed to be principal_paid, hardcoded for testing
		#blockdata.tlctousdc=D.Decimal(blockdata.get_TLC_USDc() ) / 100000000 
		#loaninfo.payTLC= loaninfo.payment / blockdata.tlctousdc
		return render(request, 'dashboard/bc_payment_details.html', {'loan': loaninfo, 'blockdata':blockdata} )

	
def loan_accounting(request):
	if request.method == 'GET':
		sort = request.GET.get('sort')
		if sort == 'month':
			history_iterable = LoanPaymentHistory.objects.annotate(order_month=Extract('pmt_date', 'month'), order_year=Extract('pmt_date','year')).all().order_by('-order_year','-order_month', '-pmt_date')
		elif sort == 'loan':
			history_iterable = LoanPaymentHistory.objects.all().order_by('loan', '-pmt_date')
		else:
			history_iterable = LoanPaymentHistory.objects.all().order_by('-pmt_date')
	return render(request, 'dashboard/loan_accounting.html', {'payments': history_iterable})
	
def credit_verify(request):
	loan_apps = ApplicationSummary.objects.all().order_by('tier', '-submission_date')
	return render(request, 'dashboard/credit_verify.html', {'apps': loan_apps})
	
def credit_verify_app(request, app_id):
	app = ApplicationSummary.objects.get(pk=app_id)
	status_list = app.STATUS_CHOICES[app.status+1:]
	return render(request, 'dashboard/credit_verify_app.html', { 'status_list': status_list })

def upload_doc(request, app_id=0):
	client = MongoClient()
	db = client.appdocs
	collection = db.documents
	if request.method == 'POST' and request.FILES['updoc']:
		doc = request.FILES['updoc'].file
		content = doc.read()
		updoc = {"filename": "Application ID: #{{ app.id }} Document", "content": content}
		updoc_id = collection.insert_one(updoc).inserted_id
		print(updoc_id)
		# TODO:
		# insert into NoSQL Model here
		# using the refkey from doc_id
		
		# model_ref = Credit_Report(source=request.user, refkey=updoc_id, app_id=app_id)
		# in order for this to work, there needs to be changes
		# in models, specifically, changing:
		# refkey = models.IntegerField() => refkey = models.Charfield(max_length=24)
		# adding:
		# app_id = models.ForeignKey(ApplicationSummary)	
	return render(request, 'dashboard/upload_doc.html', {})
	
def certify(request):
	#req_basic = NewRequestSummary.objects.filter(status=3).order_by('-submitted')
	req_standard = NewRequestSummary.objects.filter(status=4).order_by('-submitted')
	#basic = ApplicationSummary.objects.filter(tier=0).exclude(status=12).order_by('-submission_date')
	standard = ApplicationSummary.objects.filter(tier=1).exclude(status=12).order_by('-submission_date')
	#cert_basic = ApplicationSummary.objects.filter(status=12, tier=0).order_by('-submission_date')
	cert_standard = ApplicationSummary.objects.filter(status=12, tier=1).order_by('-submission_date')
	return render(request, 'dashboard/certify.html', {'standard': standard, 'req_standard': req_standard, 'cert_standard': cert_standard})# 'basic': basic, 'req_basic': req_basic, 'cert_basic': cert_basic})
	
def certify_app(request, app_id):
	app = ApplicationSummary.objects.get(pk=app_id)
	credit = CreditRequest.objects.get(application=app)
	return render(request, 'dashboard/workflow_detail.html', {'app': app, 'credit': credit})
		
def calculate_interest(last_paid_date, paid_date, principal_bal, int_rate, conversion=0):
	if conversion == 0:
		date_delta = paid_date.date() - last_paid_date.date()
	elif conversion == 1:
		pd = datetime.datetime.strptime(paid_date, "%Y-%m-%d")
		date_delta = pd.date() - last_paid_date.date()
		
	interest_accrued = date_delta.days * principal_bal * ((int_rate / 100) / 365)
	return round(interest_accrued, 2)
	
def loan_payments(request, loan_id='0'):
	if loan_id[:3] == 'vd_':
		loan=NewLoan.objects.get(pk=loan_id[3:])
		return render(request, 'dashboard/loan_details.html', {'loan': loan})
	elif not 'vd_' in loan_id and loan_id != '0':
		loan = NewLoan.objects.get(pk=loan_id)
		try:
			most_recent = LoanPaymentHistory.objects.filter(wallet=loan.loan_wallet).order_by('-pmt_date')[0].pmt_date
			if request.is_ajax():
				form_name = 'PaymentForm'
				pmt_date = request.POST['pmt_date']
				interest_calc = calculate_interest(most_recent, pmt_date, loan.principal_balance, loan.loan_intrate_current, 1)
				return JsonResponse({'interest_calc': interest_calc})
			
			elif request.method == 'POST' and not request.is_ajax():
				form = PaymentForm(request.POST)
				form_name = 'PaymentForm'
				if form.is_valid():
					obj = form.save(commit=False)
					obj.wallet = loan.loan_wallet
					obj.loan = loan
					obj.interest_pmt = calculate_interest(most_recent, obj.pmt_date, loan.principal_balance, loan.loan_intrate_current, 0)
					obj.principal_pmt = obj.pmt_total - obj.interest_pmt
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
				form_name = 'PaymentForm'
			return render(request, 'dashboard/make_payment.html', {'loan':loan, 'form':form, 'form_name': form_name})
		except:
			if request.method == 'POST':
				form = FirstPaymentForm(request.POST)
				form_name = 'FirstPaymentForm'
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
				form = FirstPaymentForm()
				form_name = 'FirstPaymentForm'
			return render(request, 'dashboard/make_payment.html', {'loan':loan, 'form':form, 'form_name': form_name})
	else:
		loan_iterable = NewLoan.objects.all()
		return render(request, 'dashboard/loan_payments.html', {'loan_iterable': loan_iterable})

def loan_details(request, loan_id):
	if loan_id[:4] == 'bsa_':
		app = ApplicationSummary.objects.get(pk=loan_id[4:])
		return render(request, 'dashboard/workflow_detail.html', {'app': app})
	else:
		loan = NewLoan.objects.get(pk=loan_id)
		return render(request, 'dashboard/loan_details.html', {'loan': loan})
		
'''##################################################
Admin Views
##################################################'''
def add_vendor(request):
	# TODO:
	# Add logic to create form for adding vendors	
	return render(request, 'admin/add_vendor.html', {})

def event_viewer(request):
	bc = events.BC()
	w3 = bc.w3
	contract_address = Web3.toChecksumAddress(bc.contract_address)
	with open('abi.json', 'r', encoding='utf-8') as abi_file:
		contract_abi = json.loads(abi_file.read())
	contract = w3.eth.contract(address=contract_address, abi=contract_abi)
	approval_filter = contract.events.Approval.createFilter(fromBlock=3255394, toBlock=4216364)
	buy_filter = contract.events.Buy.createFilter(fromBlock=3255394, toBlock=4216364)
	loan_payment_filter = contract.events.LoanPayment.createFilter(fromBlock=3255394, toBlock=4216364)
	ownership_filter = contract.events.OwnershipTransferred.createFilter(fromBlock=3255394, toBlock=4216364)
	transfer_filter = contract.events.Transfer.createFilter(fromBlock=3255394, toBlock=4216364)
	approval_events = approval_filter.get_all_entries()
	buy_events = buy_filter.get_all_entries()
	loan_payment_events = loan_payment_filter.get_all_entries()
	ownership_events = ownership_filter.get_all_entries()
	transfer_events = transfer_filter.get_all_entries()
	context = {
		'approval_events': approval_events,
		'buy_events': buy_events,
		'loan_payment_events': loan_payment_events,
		'ownership_events': ownership_events,
		'transfer_events': transfer_events,
	}
	return render(request, 'admin/event_viewer.html', context)

def bc_explorer(request):
	bc = explorer.BC()
	w3 = bc.w3
	tx = web3.eth.Eth(w3) 
	contract_address = Web3.toChecksumAddress(bc.contract_address)
	transaction = {}
	net = 'ropsten.' # Set to '' to target mainnet
	for hash in reversed(rop_tx):
		receipt = tx.getTransactionReceipt(hash)
		tx_data = tx.getTransaction(hash)
		try:
			f_raw = tx_data.input[2:10]
			function = functions[f_raw]
		except:
			function = 'N/a'
		try:
			data = receipt.logs[0]['data']
			hint = int(data[2:], 16)
		except:
			data = receipt.logs
			hint = None
		transaction[hash] = {
			'from': receipt['from'],
			'to': receipt['to'],
			'data': data,
			'hint': hint,
			'input': tx_data.input,
			'function': function,
			'f_raw': f_raw,
		}
	context = {
		'net': net,
		'transaction': transaction,
	}
	return render(request, 'admin/bc_explorer.html', context)

def token_audit(request):
	bc = audit.BC()
	w3 = bc.w3
	contract_address = Web3.toChecksumAddress(bc.contract_address)
	with open('abi.json', 'r', encoding='utf-8') as abi_file:
		contract_abi = json.loads(abi_file.read())
	contract = w3.eth.contract(address=contract_address, abi=contract_abi)
	try:
	#	transfer_filter = contract.events.Transfer.createFilter(fromBlock=0)
		transfer_filter = my_contract.events.Transfer.createFilter(fromBlock=4340299, toBlock=4615429)
	except:
		context = {'message': 'Oops! Something went wrong'}
		return render(request, 'admin/audit.html', context)
	tx = web3.eth.Eth(w3)
	context = {}
	addresses = ['0x0000000000000000000000000000000000000000']
	zero_addresses = []
	zero_sum = 0
	tracked_balance = 0
	for transfer in transfer_filter.get_all_entries():
		if transfer['args']['from'].lower() not in addresses:
			addresses.append(transfer['args']['from'].lower())
		if transfer['args']['to'].lower() not in addresses:
			addresses.append(transfer['args']['to'].lower())
	for x in main_tx:
		receipt = tx.getTransactionReceipt(x)
		try:
			if receipt['from'].lower() not in addresses:
				addresses.append(receipt['from'].lower())
			if receipt['to'].lower() not in addresses:
				addresses.append(receipt['to'].lower())
		except:
			pass
	for addr in addresses:
		try:
			addr = web3.Web3.toChecksumAddress(addr)
			token_balance = my_contract.call().balanceOf(addr)
			if not token_balance == 0:
				tracked_balance += token_balance
				context[addr] = [token_balance]
			else:
				zero_bal += 1
				zero_addresses.append(addr)
		except:
			pass

	return render(request, 'admin/audit.html', context)
	
'''##################################################
PDF Generation Views
##################################################'''
def link_callback(uri, rel):
	"""
	Convert HTML URIs to absolute system paths so xhtml2pdf can access those
	resources
	"""
	# use short variable names
	sUrl = settings.STATIC_URL      # Typically /static/
	sRoot = settings.STATIC_ROOT    # Typically /home/userX/project_static/
	mUrl = settings.MEDIA_URL       # Typically /static/media/
	mRoot = settings.MEDIA_ROOT     # Typically /home/userX/project_static/media/

	# convert URIs to absolute system paths
	if uri.startswith(mUrl):
		path = os.path.join(mRoot, uri.replace(mUrl, ""))
	elif uri.startswith(sUrl):
		path = os.path.join(sRoot, uri.replace(sUrl, ""))
	else:
		return uri  # handle absolute uri (ie: http://some.tld/foo.png)

	# make sure that file exists
	if not os.path.isfile(path):
		raise Exception(
			'media URI must start with %s or %s' % (sUrl, mUrl)
			)
	return path

def pdfgenerate(request, app_id):
	app = ApplicationSummary.objects.get(pk=app_id)
	credit = CreditRequest.objects.get(application=app)
	template_path = 'pages/pdflayout.html'
	context = {'app': app, 'credit': credit}
	# Create a Django response object, and specify content_type as pdf
	response = HttpResponse(content_type='application/pdf')
	#Uncomment the below command if you want the PDF to download rather than http display.
	#response['Content-Disposition'] = 'attachment; filename="report.pdf"'
	# find the template and render it.
	template = get_template(template_path)
	html = template.render(context)

	# create a pdf
	pisaStatus = pisa.CreatePDF(
		html, dest=response, link_callback=link_callback)
	# if error then show some funny view
	if pisaStatus.err:
		return HttpResponse('We had some errors <pre>' + html + '</pre>')
	return response
	
'''##################################################
# Form Views
##################################################'''
# handle_pop_add and new_field are the views that manage the '+' icon next to FK fields
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
	new_field=field_name
	if 'addr' in field_name:
		return handle_pop_add(request, AddressForm, new_field)
	elif 'borrower' in field_name:
		return handle_pop_add(request, BorrowerInfoForm, new_field)
	elif 'emp' in field_name:
		return handle_pop_add(request, EmploymentIncomeForm, new_field)

# Form for Loan Apply (Contact Form)
class LoanApplyWizard(SessionWizardView):
	# Function to send the form some initial values
	def get_form_initial(self, step):
		user = self.request.user
		if step == '0':
			self.initial_dict = {'user': user}
			try:
				person = Person.objects.get(user=user)
			except:
				person = None
				pass
			try:
				user_apps = NewRequestSummary.objects.filter(user=user).order_by('-submitted')
				most_recent = user_apps.first()
			except:
				most_recent = None
				pass
			if person:
				self.initial_dict.update({
					'name_first': person.name_first,
					'name_middle': person.name_middle,
					'name_last': person.name_last,
					'phone': person.phone,
					'email_address': person.email_address,
				})
			if most_recent:
				self.initial_dict.update({
					'name_first': most_recent.contact.name_first,
					'name_middle': most_recent.contact.name_middle,
					'name_last': most_recent.contact.name_last,
					'phone': most_recent.contact.phone,
					'email_address': most_recent.contact.email_address,
				})
			
		if step == '1':
			self.initial_dict = {'user': self.request.user}

		return self.initial_dict

	def get_form(self, step=None, data=None, files=None):
		form = super(LoanApplyWizard, self).get_form(step, data, files)
		
		if step is None:
			step = self.steps.current

		if step == '1':
			try:
				mut = form.data.copy()
				x = mut['1-rent'].replace(',','')
				mut['1-rent'] = x
				form.data = mut
				self.request.POST = form.data
			except: 
				pass

		if step == '2':
			try:
				mut = form.data.copy()
				x = mut['2-original_amount'].replace(',','')
				mut['2-original_amount'] = x
				x = mut['2-current_balance'].replace(',','')
				mut['2-current_balance'] = x
				form.data = mut
				self.request.POST = form.data
			except:
				pass

		if step == '3':
			try:
				mut = form.data.copy()
				x = mut['3-amount_desired'].replace(',','')
				mut['3-amount_desired'] = x
				x = mut['3-cash_back_desired'].replace(',','')
				mut['3-cash_back_desired'] = x
				x = mut['3-payment_desired'].replace(',','')
				mut['3-payment_desired'] = x
				form.data = mut
				self.request.POST = form.data
			except:
				pass

		if step == '4':
			try:
				mut = form.data.copy()
				x = mut['4-annual_income'].replace(',','')
				mut['4-annual_income'] = x
				x = mut['4-net_worth'].replace(',','')
				mut['4-net_worth'] = x
				form.data = mut
				self.request.POST = form.data
			except:
				pass	
		return form

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
		
			def payment_calc(Pv, r, n):
				predec = 365/12
				dec = D.Decimal(str(predec))
				n = 12 * n
				R = (1+(r/100/365))**(dec)-1
				P = (Pv * R)/(1-(1+R)**(-n))
				return round(P, 2)

			str_amount = str(d.amount_desired)
			str_intrate = str(d.intrate_desired)
			term = d.term_desired

			if term == 4:
				str_term = '1 Year'
			else:
				str_term = d.TERM_CHOICES[term][1]

			try:
				split_term = str_term.split('Less than ')[1][:2]
			except:
				split_term = str_term[:2]
				pass	

			# retrieves estimated payment
			est_payment = payment_calc(d.amount_desired, d.intrate_desired, int(split_term))
			
			# sends email (to USER) when data is submitted and validated
			# WIP
			send_mail(
				# subject line
				'Your The LendingCoin, Inc. Loan Refinancing Query',
				
				# message
				('Greetings %s %s,\n\nThe LendingCoin, Inc. received your Commercial Loan Refinancing Expression of Interest and is processing the information you submitted. It has been routed to the refinancing committee for review and you will be hearing from us soon.\n\nAt The LendingCoin, Inc., we are excited to be able to provide you and others with the opportunity to be considered for this alternative to traditional refinancing that allows you better terms, quicker and more responsive considerations, and the benefit of the transparency of the blockchain empowered processes employed at The LendingCoin, Inc.\n\nBased on your requested loan, a loan of $%s for %s(s) at %s %% would make your payment approximately $%s.\n\nWe look forward to disussing your refinancing needs in detail. If you have any need to talk to us before we are able to contact you, please don\'t hesitate.\n\nSincerely,\n\nDavid Slonaker\nChief Financial Officer\n\nThe LendingCoin, Inc.\n1550 S. Cloverdale Rd.\nBoise, ID 83709\n(208) 401-9596\nthelendingcoin.com') % (a.name_first, a.name_last, str_amount, str_term, str_intrate, str(est_payment)), 

				# 'from' email address
				'loan-dept@thelendingcoin.com',
				
				# 'to' email address(es)
				[a.email_address, 'loan-dept@thelendingcoin.com', 'rich@thelendingcoin.com', 'quoc@thelendingcoin.com', 'paul@thelendingcoin.com']
			)
			
			# sends email (to STAFF) when data is submitted and validated
			# WIP
			send_mail(
				# subject line
				'New Refinancing Query',
			
				# message
				('Greetings staff,\n\nThe LendingCoin, Inc. has received an Expression of Interest in obtaining more information about refinancing a commercial loan from %s %s.\n\n Contact Information\n\nName: %s %s\nPhone: %s\nEmail: %s\n\nProperty Information\n\nProperty Type: %s\nProperty Address: %s\nRent: $%s\nProperty Age: %s\n\nCurrent Mortgage\n\nDate Loan Originated: %s\nCurrent Loan Type: %s\nOriginal Amount: $%s\nCurrent Balance: $%s\nCurrent Term: %s\nCurrent Interest Rate: %s %%\nLate Payments: %s\n\nDesired Mortgage\n\nAmount Desired: $%s\nCash Back Desired: $%s\nLoan Currency: %s\nLoan Type Desired: %s\nPayment Desired: $%s\nInterest Rate Desired: %s %%\nTime Frame Desired: %s\nTerm Desired: %s\n\nBorrower Information\n\nBorrower Type: %s\nAnnual Income: $%s\nNet Worth: $%s\nFICO Score: %s\n\nAt your earliest opportunity, please review their Expression of Interest and process their submission as appropriate. This Expression of Interest can be reviewed by logging into The LendingCoin, Inc. Refinancing Dashboard and navigating to \'Loan Requests\'\n\nRegards,\n\nThe LendingCoin, Inc.') % (a.name_first, a.name_last, a.name_first, a.name_last, a.phone, a.email_address, b.TYPE_CHOICES[b.property_type][1], b.property_address, b.rent, b.property_age, c.date_loan_originated, c.TYPE_CHOICES[c.current_loan_type][1], c.original_amount, c.current_balance, c.current_term, c.current_intrate, c.LATE_CHOICES[c.late_payments][1], d.amount_desired, d.cash_back_desired, d.loan_currency, d.TYPE_CHOICES[d.loan_type_desired][1], d.payment_desired, d.intrate_desired, d.TIMEFRAME_CHOICES[d.time_frame][1], d.TERM_CHOICES[d.term_desired][1], e.B_TYPE_CHOICES[e.type][1], e.annual_income, e.net_worth, e.FICO_CHOICES[e.fico][1]),

				# 'from' email address
				'loan-dept@thelendingcoin.com',

				# 'to' email address(es)
				['loan-dept@thelendingcoin.com', 'rich@thelendingcoin.com', 'quoc@thelendingcoin.com', 'paul@thelendingcoin.com']
			)	

		return render(self.request, 'pages/loan_apply_done.html', {'name': a.name_first + ' ' + a.name_last} )

# Django FormWizard view for Basic Application
'''class BasicWizard(NamedUrlSessionWizardView):
	# Function to send the form some initial values
	def get_form_initial(self, step):
		user = self.request.user
		if step == '3' or step == '4':
			self.initial_dict = {'user': user}
		return self.initial_dict
		
	def get_context_data(self, form, value=0, step=None, **kwargs):
		context = super(BasicWizard, self).get_context_data(form=form, step=step, **kwargs)
		if self.steps.current == '1':
			try:
				self.request.session['request_id'] = self.kwargs['value']
			except:
				pass
		return context
	
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
			g = self.get_form(step='7', data=g_data).save(commit=False)
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
			
			# Determines if applicant is borrower or coborrower, 
			# and sets the BorrowerInfo to the correct field in AcknowledgeAgree
			g.source = self.request.user
			if d.borrower_type == 0:
				g.borrower = d
			elif d.borrower_type == 1:
				g.coborrower = d
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
			
			if 'request_id' in self.request.session:
				request_id = self.request.session['request_id']
				request = NewRequestSummary.objects.get(pk=request_id)
				request.status = 5
				request.save()
			
			# Sends email when data is submitted to DB
			send_mail(
				'A Basic application has been submitted', # subject line - will change to add more info
				'This is where the application details will go', # message - will add more info to this
				'noreply@tlc.com', # 'from' email address
				['cto@mediacoin.stream'] # recipient email address
			)
			
		return render(self.request, 'pages/loan_apply_done.html')'''
		
# Form for Standard application
class StandardWizard(NamedUrlSessionWizardView):
	# Function to send the form some initial values
	def get_form_initial(self, step):
		user = self.request.user
		if (
			step == '3' or step == '4' or step == '5' or 
			step == '7' or step == '10'
		):
			self.initial_dict = {'user': user}
		return self.initial_dict
		
	def get_context_data(self, form, value=0, step=None, **kwargs):
		context = super(StandardWizard, self).get_context_data(form=form, step=step, **kwargs)
		if self.steps.current == '1':
			try:
				self.request.session['request_id'] = self.kwargs['value']
			except:
				pass
		return context
		
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
			
			g.source = self.request.user
			g.save()
			
			# Saves Foreign Keys for 'AssetSummaryForm'
			f.source = self.request.user
			f.acct1 = e
			f.employment_income = d
			f.managed_property = g
			f.save()
			
			i.source = self.request.user
			i.save()
			
			# Saves Foreign Keys for 'BorrowerInfoForm'
			j.user = self.request.user
			j.source = self.request.user
			j.business = a
			j.declarations = i
			j.save()
			
			# Determines if applicant is borrower or coborrower, 
			# and sets the BorrowerInfo to the correct field in AcknowledgeAgree
			k.source = self.request.user
			if j.borrower_type == 0:
				k.borrower = j
			elif j.borrower_type == 1:
				k.coborrower = j
			k.save()
			
			# Creates 'ApplicationSummary' off of step data
			# Will not work, need data for borrower
			summary = aps(
				user = self.request.user,
				source = self.request.user,
				property = c,
				borrower = j,
				asset_summary = f,
				acknowledge = k,
				tier = 1,
			)
			summary.save()
			
			# Saves Foreign Keys to 'CreditRequestForm'
			h.source = self.request.user
			h.borrower = j
			h.application = summary
			h.save()
			
			# Changes the status of the LoanApply request to 'Submitted'
			if 'request_id' in self.request.session:
				request_id = self.request.session['request_id']
				request = NewRequestSummary.objects.get(pk=request_id)
				request.status = 5
				request.save()
			
			# Sends email when data is submitted to DB
			'''send_mail(
				'A Standard application has been submitted', # subject line - will change to add more info
				'This is where the application details will go', # message - will add more info to this
				'noreply@tlc.com', # 'from' email address
				['cto@mediacoin.stream'] # recipient email address
			)'''
			
		return render(self.request, 'pages/loan_apply_done.html')
		
# Form to convert application into a loan
# TODO: This code was reinstated due to the need for a hotfix to the
# app -> loan conversion process. There are still issues that need
# addressed:
# 	- NewLoan() requires a Contract FK object, however, since we don't have that data, a Contract object is created and assigned below. This will change once we figure out the ipfs/mongodb interactions.
# 	- This process is the old "one-button-conversion" process. It will be replaced/modified when we figure out the architecture of the new process.
class ConversionWizard(SessionWizardView):
	def done(self, form_list, **kwargs):
		loan = NewLoan
		contract = Contract
		# Used to calculate payment_due_date - Removed,
		# it should allow the LO to set the due date manually instead.
		# curr_date = datetime.datetime.now()
		# due_date = curr_date + datetime.timedelta(days=15)
		
		# a, 0 = LoanTerms
		# b, 1 = LoanWallet
		
		a_data = self.storage.get_step_data('0')
		a_valid = self.get_form(step='0', data=a_data).is_valid()
		b_data = self.storage.get_step_data('1')
		b_valid = self.get_form(step='1', data=b_data).is_valid()
		
		if (
			a_valid and b_valid
		):
			a = self.get_form(step='0', data=a_data).save(commit=False)
			b = self.get_form(step='1', data=b_data).save(commit=False)
			
			app_id = kwargs['app_id']
			app_id = app_id[3:]
			
			a.application = ApplicationSummary.objects.get(pk=app_id)
			a.save()
			
			b.wallet = a.application.user
			b.save()
	
			new_contract = contract(
				source = a.application.user,
				refkey = 1,
			)
			new_contract.save()
			
			def payment_calc(Pv, r, n):
				predec = 365/12
				dec = D.Decimal(str(predec))
				R = (1+(r/100/365))**(dec)-1
				P = (Pv * R)/(1-(1+R)**(-n))
				return round(P, 2)
			
			new_loan = loan(
				user = a.application.user,
				contract = Contract.objects.get(pk=1), # hardcoded for testing, will need changed
				borrower = a.application.borrower,
				coborrower = a.application.coborrower,
				loan_terms = a,
				# formula for payment_due calculation here (interest daily):
				#https://superuser.com/questions/871404/what-would-be-the-the-mathematical-equivalent-of-this-excel-formula-pmt
				payment_due = payment_calc(a.loan_amount, a.int_rate, a.months_left),
				# payment_due_date calculated above
				payment_due_date = 1,
				payments_left = a.months_left,
				principal_balance = a.loan_amount,
				loan_intrate_current = a.int_rate,
				principal_paid = 0, # will be 0 on creation of loan
				interest_paid = 0, # will be 0 on creation of loan
				loan_wallet = b,
				TLC_balance = 0, # unsure of what this will be, ask Ian
			)
			new_loan.save()
			
			a.application.status = 12
			a.application.tier = 2
			a.application.save()
			
		return HttpResponseRedirect('/submit_loan')
		
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
