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
admin.site.register(RefinanceInfo)
admin.site.register(PropertyInfo)
admin.site.register(BorrowerInfo)
admin.site.register(CreditRequest)
admin.site.register(Declaration)
admin.site.register(TransactionDetails)
admin.site.register(AcknowledgeAgree)

# Tier 2
admin.site.register(EmploymentIncome)
admin.site.register(BankAccount)
admin.site.register(Bond)
admin.site.register(Stock)
admin.site.register(Vehicle)
admin.site.register(AssetSummary)
admin.site.register(Debt)
admin.site.register(ManagedProperty)
admin.site.register(Alimony)
admin.site.register(ChildSupport)
admin.site.register(SeparateMaint)
admin.site.register(LiabilitySummary)
admin.site.register(ALSummary)

# Loan Officer
admin.site.register(LenderInfo)
admin.site.register(LoanTerms)
admin.site.register(LoanWorkflow)
admin.site.register(LoanSummary)