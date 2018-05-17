from django.contrib import admin
from .models import Loan, Loan_Data, Loan_Request, Loan_Workflow

# Register your models here.
admin.site.register(Loan)
admin.site.register(Loan_Data)
admin.site.register(Loan_Request)
admin.site.register(Loan_Workflow)