from django import template
from wwwtlc.ethereum import BC

register = template.Library()

@register.filter
def get_loan_bal(value):
	blockdata = BC()
	blockdata.loanbal=blockdata.get_loan_bal(value) / 100
	
	return blockdata.loanbal