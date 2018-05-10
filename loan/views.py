from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from .forms import LoanForm, LoanDataForm, AddressForm, PersonForm

#new view that passes information depending on last form 
# not working, view controller sets variable everytime loan_apply is called, but cant define view_controller outside of function(then it's out of scope)
# possibly going to implement something like http://django-formtools.readthedocs.io/en/latest/wizard.html
def loan_apply(request):
	view_controller = 0
	
	if view_controller == 0:
		if request.method == 'POST':
			address = AddressForm(request.POST)
			if address.is_valid():
				address.save()
				view_controller = 1
				return render(request, 'pages/loan_apply.html', {'form':address})#HttpResponseRedirect('home')
		else:
			address = AddressForm()
			view_controller = 1
		return render(request, 'pages/loan_apply.html', {'form':address})
	
	if view_controller == 1:
		if request.method == 'POST':
			person = PersonForm(request.POST)
			if person.is_valid():
				person.save()
				view_controller = 2
				return HttpResponseRedirect('pages/loan_apply.html')
		else:
			person = PersonForm()
			view_controller = 2
		return render(request, 'pages/loan_apply.html', {'form':person})
	
	if view_controller == 2:
		if request.method == 'POST':
			loan_data = LoanDataForm(request.POST)
			if loan_data.is_valid():
				loan_data.save()
				return HttpResponseRedirect('home')
		else:
			loan_data = LoanDataForm()
		return render(request, 'pages/loan_apply.html', {'form':loan_data})