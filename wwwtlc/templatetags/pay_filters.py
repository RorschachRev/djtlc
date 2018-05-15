from django import template
register = template.Library()
import locale

@register.inclusion_tag(name='templates/pages/pay.html')

def add_currency_symbol(value):
	currstr = value
	locale.setlocale( locale.LC_ALL, '' )
	currstr = locale.currency(currstr)
	
	return currstr
	
	
	