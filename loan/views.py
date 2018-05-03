from django.shortcuts import render
from django.http import HttpResponseRedirect

from .forms import LoanForm

# Create your views here.
def loan_apply(request):
	if request.method == 'POST':
		form = LoanForm(request.POST)
		if form.is_valid():
			return HttpResponseRedirect('home')
	else:
		form = LoanForm()
	return render(request, 'pages/loan_apply.html', {'form': form})