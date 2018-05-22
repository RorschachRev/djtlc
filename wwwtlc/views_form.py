from django import forms
from django.conf import settings
from django.shortcuts import render, get_object_or_404
from django.core.mail import send_mail

def account(request):
	
	return render(request, 'pages/account.html')
	
def wallet(request):
	return render(request, 'pages/wallet.html')	
