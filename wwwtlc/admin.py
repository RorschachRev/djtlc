from django.contrib import admin
from .models import Person, Address, Verified, Wallet
from .models_loan_app import *

# Register your models here.
admin.site.register(Person)
admin.site.register(Address)
admin.site.register(Verified)
admin.site.register(Wallet)

# Tier 1
admin.site.register(BusinessInfo)
#admin.site.register(ExpenseInfo)
admin.site.register(ConstructionInfo)
admin.site.register(PropertyInfo)
admin.site.register(BorrowerInfo)
admin.site.register(CreditRequest)
admin.site.register(Declaration)
admin.site.register(AcknowledgeAgree)

# Tier 2
admin.site.register(EmploymentIncome)
admin.site.register(BankAccount)
admin.site.register(AssetSummary)
admin.site.register(ManagedProperty)

# Loan Officer
admin.site.register(LenderInfo)
admin.site.register(LoanTerms)
#admin.site.register(LoanWorkflow)
admin.site.register(ApplicationSummary)
admin.site.register(LoanSummary)
admin.site.register(NewLoan)
admin.site.register(LoanPaymentHistory)