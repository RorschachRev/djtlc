from django.shortcuts import render
from django.http import HttpResponseRedirect

from .forms import LoanForm, LoanDataForm

# Create your views here.
def loan_apply(request):
	if request.method == 'POST':
		form1 = LoanDataForm(request.POST)
		#form2 = LoanForm(request.POST) # unsure why commented out
		if form.is_valid():
			return HttpResponseRedirect('home')
	else:
		form1 = LoanDataForm()
		#form2 = LoanForm() # unsure why commented out, also deleted from return, so to show, add   , 'formLoan':form2    inside the curly braces of the render statement
	return render(request, 'pages/loan_apply.html', {'formLoanData':form1})