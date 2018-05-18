from django.shortcuts import render
from django.http import HttpResponseRedirect
from formtools.wizard.views import SessionWizardView
#from .models import Loan_Data, Address, Person
from .forms import LoanRequestForm, LoanDataForm, AddressForm, PersonForm

#view to use Django FormWizard to create the multi-step form (LoanRequest -> LoanData -> Address -> Person(contact for LoanData))
class LoanApplyWizard(SessionWizardView):
	def done(self, form_list, **kwargs):
		# a, 0 = LoanRequest
		# b, 1 = LoanData
		# c, 2 = Address
		# d, 3 = Person
		
		# This block of code binds data from form to form itself, and validates the data
		a_data = self.storage.get_step_data('0')
		a_valid = self.get_form(step='0', data=a_data).is_valid()
		b_data = self.storage.get_step_data('1')
		b_valid = self.get_form(step='1', data=b_data).is_valid()
		c_data = self.storage.get_step_data('2')
		c_valid = self.get_form(step='2', data=c_data).is_valid()
		d_data = self.storage.get_step_data('3')
		d_valid = self.get_form(step='3', data=d_data).is_valid()
		
		# This block of code sets the foreign keys of each table to the entries entered in the previous form step, if the data is valid
		if a_valid and b_valid and c_valid:
			a = self.get_form(step='0', data=a_data).save()
			b = self.get_form(step='1', data=b_data).save(commit=False)
			c = self.get_form(step='2', data=c_data).save()
			d = self.get_form(step='3', data=d_data).save(commit=False)
			
			d.address = c
			d.save()
		
			b.loan_address = c
			b.contact_person = d
			b.save()
			
		return render(self.request, 'pages/loan_apply_done.html', {'name': d.name_first + ' ' + d.name_last} )