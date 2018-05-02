from django.shortcuts import render
from django.http import HttpResponseRedirect

from .form import LoanForm

# Create your views here.
def loan_apply_done(request):
	if request.method == 'POST':
		form = LoanForm(request.POST)
		if form.is_valid():
			return HttpResponseRedirect('/home/')
			
	else:
		form = LoanForm()
	return render(request, 'home.html', {}) #todo
	
def loan_apply(request):
	return render(request, 'loan_apply.html', {'form': form})