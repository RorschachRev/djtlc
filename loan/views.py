from django.shortcuts import render
from django.http import HttpResponseRedirect

from .forms import LoanForm, LoanDataForm

# Create your views here.
def loan_apply(request):
	if request.method == 'POST':
		form1 = LoanDataForm(request.POST)
		#form2 = LoanForm(request.POST)
		if form.is_valid():
			return HttpResponseRedirect('home')
	else:
		form1 = LoanDataForm()
		#form2 = LoanForm()
	return render(request, 'pages/loan_apply.html', {'formLoanData':form1 })