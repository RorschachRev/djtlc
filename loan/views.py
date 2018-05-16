from django.shortcuts import render
from django.http import HttpResponseRedirect
from formtools.wizard.views import SessionWizardView
from .models import Loan, Loan_Data, Address, Person
from .forms import LoanForm, LoanDataForm, AddressForm, PersonForm
from django.contrib.auth.models import User

#view to use Django FormWizard to create the multi-step form (Address -> Person -> LoanData)
class LoanApplyWizard(SessionWizardView):
	def done(self, form_list, **kwargs):
		
		# This block of code binds data from form to form itself, and validates the data
		a_data = self.storage.get_step_data('0')
		a_valid = self.get_form(step='0', data=a_data).is_valid()
		b_data = self.storage.get_step_data('1')
		b_valid = self.get_form(step='1', data=b_data).is_valid()
		c_data = self.storage.get_step_data('2')
		c_valid = self.get_form(step='2', data=c_data).is_valid()
		
		# This block of code sets the foreign keys of each table to the entries entered in the previous form step, if the data is valid
		if a_valid and b_valid and c_valid:
			a = self.get_form(step='0', data=a_data).save()
			b = self.get_form(step='1', data=b_data).save(commit=False)
			c = self.get_form(step='2', data=c_data).save(commit=False)
		
			b.address = a
			b.save()
			c.loan_address = a
			c.contact_person = b
			c.save()
			
		return HttpResponseRedirect('/')