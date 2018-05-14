from django.shortcuts import render
from django.http import HttpResponseRedirect
from formtools.wizard.views import CookieWizardView
from .forms import LoanForm, LoanDataForm, AddressForm, PersonForm
from django.contrib.auth.models import User

#view to use Django FormWizard to create the multi-step form (Address -> Person -> LoanData)
class LoanApplyWizard(CookieWizardView):
	def get_form(self, step=None, data=None, files=None):
		form = super(LoanApplyWizard, self).get_form(step, data, files)
		
		if step == None:
			step = self.steps.current
		
		if step == '0':
			if form.is_valid():
				form.save() #saves the address form to the address model
			
		if step == '1':
			form.address = self.storage.get_step_data('0') #pulls address model into Person Form
			
			if form.is_valid():
				form.save()
		
		if step == '2':
			form.contact_person = self.storage.get_step_data('1') #pulls address model into LoanDataForm
			if form.is_valid():
				form.save()
		
		return form
	def done(self, form_list, **kwargs):
		return render(self.request, 'pages/loan_apply.html', {'form':[form.cleaned_data for form in form_list]})

