from django.contrib import admin
from .models import Loan, Loan_Data

# Register your models here.
admin.site.register(Loan)
admin.site.register(Loan_Data)
