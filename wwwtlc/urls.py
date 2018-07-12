''' 
Original Dashboard URLs:

    url(
        r'^dashboard/new_apps/$',
        views.new_apps,
        name='new_apps'
),
    url(
        r'^dashboard/in_progress_apps/$',
        views.in_progress_apps,
        name='in_progress_apps'
),
    url(
        r'^dashboard/overdue/$',
        views.overdue,
        name='overdue'
),
    url(
        r'^dashboard/loans/$',
        views.dashboard_loans,
        name='loans'
),
    url(
        r'^dashboard/loans/(?P<pk>.+)/$',
        views.loan_details,
        name='loan_details'
),
'''
from django.conf.urls import url
from django.conf import settings
from django.contrib import admin
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.views.generic.base import TemplateView
from wwwtlc import views
from wwwtlc.forms import *
from wwwtlc import views_form
from wwwtlc.views import TierOneWizard, TierTwoWizard
from loan import views as views_loan
from loan.views import LoanApplyWizard
from loan.forms import PersonForm, LoanDataForm, LoanRequestForm

# below is for testing the NamedUrlSessionsView for the formtools app
# https://django-formtools.readthedocs.io/en/latest/wizard.html#usage-of-namedurlwizardview
tier_one_forms = (
	(1, AddressForm),
	(2, BusinessInfoForm),
	(3, ConstructionInfoForm),
	(4, RefinanceInfoForm),
	(5, PropertyInfoForm),
	(6, BorrowerInfoForm),
	(7, CreditRequestForm),
	(8, DeclarationForm),
	(9, TransactionDetailsForm),
	(10, AcknowledgeAgreeForm),
)

tier_two_forms = (
	(1, AddressForm),
	(2, BusinessInfoForm),
	(3, ConstructionInfoForm),
	(4, RefinanceInfoForm),
	(5, PropertyInfoForm),
	(6, EmploymentIncomeForm),
	(7, BankAccountForm),
	(8, BondForm),
	(9, StockForm),
	(10, VehicleForm),
	(11, AssetSummaryForm),
	(12, DebtForm),
	(13, ManagedPropertyForm),
	(14, AlimonyForm),
	(15, ChildSupportForm),
	(16, SeparateMaintForm),
	(17, LiabilitySummaryForm),
	(18, ALSummaryForm),
	(19, BorrowerInfoForm),
	(20, CreditRequestForm),
	(21, DeclarationForm),
	(22, TransactionDetailsForm),
	(23, AcknowledgeAgreeForm),
)

tier_one_wizard = TierOneWizard.as_view(tier_one_forms, url_name='tier_one_step', template_name='pages/tier1_app.html')

tier_two_wizard = TierTwoWizard.as_view(tier_two_forms, url_name='tier_two_step', template_name='pages/tier2_app.html')

urlpatterns = [
    url(
        r'^$', 
        views.home, 
        name='home'
),
    url(
        r'^signup/$',
        views.signup, 
        name='signup'
),
    url(
        r'^login/$', 
        auth_views.login, 
        {'template_name': 'pages/login.html'}, 
        name='login'
),
    url(
        r'^logout/$', 
        auth_views.logout, 
        {'template_name': 'pages/logout.html'},
        name='logout'
),
    url(
        r'^account.html$', 
        views.account, 
        name='account'
),
    url(
        r'^wallet.html$', 
        views.wallet, 
        name='wallet'
),
    url(
        r'^loan.html$', 
        views.loan, 
        name='loan'
),
    url(
        r'^pay.html/(?P<loan_id>\d+)/$',  #allows the specific row's data id to be passed from loan.html to pay.html
        views.pay, 
        name='pay'
),
    url(
        r'^payhistory.html$', 
        views.payhistory, 
        name='payhistory'
),
    url(
        r'^test.html$', 
        views.test, 
        name='test'
),
    url(
        r'^loan_apply_done.html$', 
        TemplateView.as_view(template_name='pages/loan_apply_done.html'), 
        name='loan_apply_done'
),
    url(
        r'^manage_requests/$',
        views.manage_requests,
        name='manage_requests'
),
    url(
        r'^manage_requests/(?P<app_id>[0-9]+)$',
        views.request_view,
        name='manage_requests'
),
    url(
        r'^workflow/$',
        views.workflow,
        name='workflow'
),
    url(
        r'^credit_verify/$',
        views.credit_verify,
        name='credit_verify'
),
    url(
        r'^package_loan/$',
        views.package_loan,
        name='package_loan'
),
    url(
        r'^manage_loan/$',
        views.manage_loan,
        name='manage_loan'
),
    url(
        r'^loan_payments/$',
        views.loan_payments,
        name='loan_payments'
),
    url(
        r'^payment_history/$',
        views.payment_history,
        name='payment_history'
),
    url(
        r'^loan_accounting/$',
        views.loan_accounting,
        name='loan_accounting'
),
    url(
        r'^admin/', 
        admin.site.urls
),
# url for LoanApply Wizard Form
    url(
        r'^loan_apply.html$', 
        LoanApplyWizard.as_view(
            [
                LoanRequestForm, 
                LoanDataForm, 
                AddressForm, 
                PersonForm
            ], 
            template_name='pages/loan_apply.html'
        ), 
        name='loan_apply'
), 
# urls for TierOneWizard form
    url(
        r'^tier_one_app/(?P<step>.+)/$', 
        tier_one_wizard,
        name='tier_one_step'
),
    url(
        r'^tier_one_app/$',
        tier_one_wizard,
        name='tier_one_app'
),
# url for TierTwoWizard form
    url(
        r'^tier_two_app/(?P<step>.+)/$',
        tier_two_wizard,
        name='tier_two_step'
),
    url(
        r'^tier_two_app/$',
        tier_two_wizard,
        name='tier_two_app'
),
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

