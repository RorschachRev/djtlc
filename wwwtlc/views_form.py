#from wwwtlc.models import Person, Loan, Loan_Data
from django.conf import settings
from django.shortcuts import render, get_object_or_404
from django.core.mail import send_mail

def loan_apply(request):
	return render(request, 'pages/loan_apply.html')
def account(request):
	return render(request, 'pages/account.html')
