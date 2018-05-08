#from wwwtlc.models import Person, Loan, Loan_Data
from wwwtlc.models import Person
from django.conf import settings
from django.shortcuts import render, get_object_or_404
from django.core.mail import send_mail

def home(request):
	return render(request, 'pages/home.html')
def loan(request):
	return render(request, 'pages/loan.html')
def wallet(request):
	return render(request, 'pages/wallet.html')
def pay(request):
	return render(request, 'pages/quoc.html')
	
