from django.contrib import admin
from .models import Person, Address, Verified, Wallet
from .models_loan_app import *
from .models_loan_app2 import *

# Register your models here.
admin.site.register(Person)
admin.site.register(Address)
admin.site.register(Verified)
admin.site.register(Wallet)

# models_loan_app
admin.site.register(CreditRequest)
#admin.site.register(ApplicantInfo)
admin.site.register(CollateralSchedule)
admin.site.register(RelationshipInfo)
admin.site.register(LenderInfo)

# models_loan_app2
admin.site.register(LoanTerms)
admin.site.register(ConstructionInfo)
admin.site.register(RefinanceInfo)
admin.site.register(PropertyInfo)
admin.site.register(EmploymentInfo)
admin.site.register(IncomeInfo)
admin.site.register(ExpenseInfo)
admin.site.register(BankAccount)
admin.site.register(Stock)
admin.site.register(Bond)
admin.site.register(Vehicle)
admin.site.register(AssetSummary)
admin.site.register(Debt)
admin.site.register(Alimony)
admin.site.register(ChildSupport)
admin.site.register(SeparateMaint)
admin.site.register(LiabilitySummary)
admin.site.register(ALSummary)
admin.site.register(Declaration)
admin.site.register(BorrowerInfo)
admin.site.register(AcknowledgeAgree)
