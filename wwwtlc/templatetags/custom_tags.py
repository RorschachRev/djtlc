from django import template
register = template.Library() #registers this tags file so that it can be called via the {% load %} template function
import locale

#uses the stackexchange solution to add the localized currency symbol onto the blockdata.loanbal
def add_currency_symbol(value):
	locale.setlocale( locale.LC_ALL, '' )
	currsym = locale.currency(value)
	
	return currsym
	
@register.filter('add_currency_symbol', add_currency_symbol) #registers the filter within django (filtername , functionname)