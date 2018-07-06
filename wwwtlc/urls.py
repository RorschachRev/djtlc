"""wwwtlc URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.views.generic.base import TemplateView
from django.conf.urls.static import static
from wwwtlc import views
from wwwtlc import views_form
from wwwtlc.views import TierOneWizard, TierTwoWizard
from wwwtlc.forms import *
from loan import views as views_loan
from loan.views import LoanApplyWizard
from loan.forms import AddressForm, PersonForm, LoanDataForm, LoanRequestForm

# below is for testing the NamedUrlSessionsView for the formtools app
# https://django-formtools.readthedocs.io/en/latest/wizard.html#usage-of-namedurlwizardview
tier_one_forms = (
	(1, BusinessInfoForm),
	(2, ConstructionInfoForm),
	(3, RefinanceInfoForm),
	(4, PropertyInfoForm),
	(5, BorrowerInfoForm),
	(6, CreditRequestForm),
	(7, DeclarationForm),
	(8, TransactionDetailsForm),
	(9, AcknowledgeAgreeForm),
)

tier_two_forms = (
	(1, BusinessInfoForm),
	(2, ConstructionInfoForm),
	(3, RefinanceInfoForm),
	(4, PropertyInfoForm),
	(5, EmploymentIncomeForm),
	(6, BankAccountForm),
	(7, BondForm),
	(8, StockForm),
	(9, VehicleForm),
	(10, AssetSummaryForm),
	(11, DebtForm),
	(12, ManagedPropertyForm),
	(13, AlimonyForm),
	(14, ChildSupportForm),
	(15, SeparateMaintForm),
	(16, LiabilitySummaryForm),
	(17, ALSummaryForm),
	(18, BorrowerInfoForm),
	(19, CreditRequestForm),
	(20, DeclarationForm),
	(21, TransactionDetailsForm),
	(22, AcknowledgeAgreeForm),
)

tier_one_wizard = TierOneWizard.as_view(tier_one_forms, url_name='tier_one_step', template_name='pages/tier1_app.html')

tier_two_wizard = TierTwoWizard.as_view(tier_two_forms, url_name='tier_two_step', template_name='pages/tier2_app.html')

urlpatterns = [
    url(
        r'^$', 
        TemplateView.as_view(template_name = 'pages/home.html'), 
        name='home'
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
        r'^dashboard/$',
        views.dashboard,
        name='dashboard'
),
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

