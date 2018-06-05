from django import template
from wwwtlc.ethereum import BC
from loan.models import Loan

register = template.Library()

@register.filter
def get_loan_bal(value):
	blockdata = BC()
	blockdata.loanbal=blockdata.get_loan_bal(value) / 100
	
	# May not have the desired effect, but is supposed to update \
	# the loan_balance of Loan with the block data
	if blockdata.loanbal:
		newbal = Loan.objects.get(loan_wallet__address=value)
		newbal.loan_balance = blockdata.loanbal
		newbal.save()
		
	return blockdata.loanbal