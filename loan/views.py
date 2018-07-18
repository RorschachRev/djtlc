from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.mail import send_mail
from formtools.wizard.views import SessionWizardView
from wwwtlc.models import NewRequestSummary

class LoanApplyWizard(SessionWizardView):
	def done(self, form_list, **kwargs):
		summary = NewRequestSummary
		
		# a, 0 = ContactRequestForm
		# b, 1 = PropertyInfoRequestForm
		# c, 2 = CurrentMortgageForm
		# d, 3 = MortgageDesiredForm
		# e, 4 = BorrowerInfoRequestForm
		
		# This block of code binds data from form to form itself, and validates the data
		a_data = self.storage.get_step_data('0')
		a_valid = self.get_form(step='0', data=a_data).is_valid()
		b_data = self.storage.get_step_data('1')
		b_valid = self.get_form(step='1', data=b_data).is_valid()
		c_data = self.storage.get_step_data('2')
		c_valid = self.get_form(step='2', data=c_data).is_valid()
		d_data = self.storage.get_step_data('3')
		d_valid = self.get_form(step='3', data=d_data).is_valid()
		e_data = self.storage.get_step_data('4')
		e_valid = self.get_form(step='4', data=e_data).is_valid()
		
		# This block of code sets the foreign keys of each table to the entries entered in the previous form step, if the data is valid
		if (
			a_valid and b_valid and c_valid and
			d_valid and e_valid
		):
			a = self.get_form(step='0', data=a_data).save()
			b = self.get_form(step='1', data=b_data).save()
			c = self.get_form(step='2', data=c_data).save()
			d = self.get_form(step='3', data=d_data).save()
			e = self.get_form(step='4', data=e_data).save()
			
			summary = summary(
				user = self.request.user,
				contact = a,
				property = b,
				curr_mortgage = c,
				desired_mortgage = d,
				borrower = e,
			)
			
			summary.save()
			
			# sends email when data is submitted and validated
			send_mail(
				# subject line - returns LoanData __str__ method
				'New Loan Request',
				
				# message
				'A new loan request has been submitted and can be found in the officer dashboard.', 
				
				# 'from' email address
				'no_reply@thelendingcoin.com',
				
				# recipient email address
				['finance@thelendingcoin.com', 'lender@thelendingcoin.com']
			)
			
		return render(self.request, 'pages/loan_apply_done.html', {'name': a.first_name + ' ' + a.last_name} )


# Old view for LoanApply form
'''#view to use Django FormWizard to create the multi-step form (LoanRequest -> LoanData -> Address -> Person(contact for LoanData))
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
			a = self.get_form(step='0', data=a_data).save(commit=False)
			b = self.get_form(step='1', data=b_data).save(commit=False)
			c = self.get_form(step='2', data=c_data).save()
			d = self.get_form(step='3', data=d_data).save(commit=False)
			
			d.address = c
			d.save()
		
			b.loan_address = c
			b.contact_person = d
			b.save()
			
			a.user = self.request.user
			a.request_data = b
			a.save()
			
			# sends email when data is submitted and validated
			send_mail(
				str(b) + ' (loan request)', # subject line - returns LoanData __str__ method
				
				# message
				'A new loan request has been submitted and can be found in the admin console:'
				'\n\nLoan_Requests (' + str(a) + '),'
				'\nLoan_Data (' + str(b) + '),' 
				'\nAddress (' + str(c) + '),'
				'\nContact Person (' + str(d) + ')', 
				
				'no_reply@tlc.com', # 'from' email address
				['loanofficer@tlc.com'] # recipient email address
			)
			
		return render(self.request, 'pages/loan_apply_done.html', {'name': d.name_first + ' ' + d.name_last} )'''