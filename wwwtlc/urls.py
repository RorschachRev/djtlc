from django.conf.urls import url
from django.conf import settings
from django.contrib import admin
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.views.generic.base import TemplateView

from wwwtlc import views
from wwwtlc.forms import *
from wwwtlc.views import LoanApplyWizard, BasicWizard, StandardWizard, LoanWizard, ConversionWizard

from loan import views as views_loan
from loan.forms import PersonForm, LoanDataForm, LoanRequestForm

# below is the forms for the NamedUrlSessionsView of the formtools app
# https://django-formtools.readthedocs.io/en/latest/wizard.html#usage-of-namedurlwizardview
basic_app_forms = (
	(1, BusinessInfoForm),
	(2, ConstructionInfoForm),
	(3, PropertyInfoForm),
	(4, BorrowerInfoForm),
	(5, CreditRequestForm),
	(6, DeclarationForm),
	(7, AcknowledgeAgreeForm),
)

standard_app_forms = (
	(1, BusinessInfoForm),
	(2, ConstructionInfoForm),
	(3, PropertyInfoForm),
	(4, EmploymentIncomeForm),
	(5, BankAccountForm),
	(6, AssetSummaryForm),
	(7, ManagedPropertyForm),
	(8, CreditRequestForm),
	(9, DeclarationForm),
	(10, BorrowerInfoForm),
	(11, AcknowledgeAgreeForm),
)
basic_wizard = BasicWizard.as_view(basic_app_forms, url_name='basic_app_step', template_name='pages/basic_app.html')#, initial={'form_id': value})

standard_wizard = StandardWizard.as_view(standard_app_forms, url_name='standard_app_step', template_name='pages/standard_app.html')

urlpatterns = [
# Core URLs
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
        r'^admin/', 
        admin.site.urls
),
    url(
        r'^test$', 
        views.test, 
        name='test'
),

# User URLs
    url(
        r'^account$', 
        views.account, 
        name='account'
),
    url(
        r'^loan$', 
        views.loan, 
        name='loan'
),
    url(
        r'^loan/(?P<loan_id>[0-9]+)/$',
        views.loan_details,
        name='loan_details'
),
    url(
        r'^wallet$', 
        views.wallet, 
        name='wallet'
),
    url(
        r'^payhistory$', 
        views.payhistory, 
        name='payhistory'
),
    url(
        r'^pay/(?P<loan_id>\d+)/$',  #allows the specific row's data id to be passed from loan.html to pay.html
        views.pay, 
        name='pay'
),

# Loan Officer URLs
    url(
        r'^loan_requests/$',
        views.loan_requests,
        name='loan_requests'
),
    url(
        r'^loan_requests/(?P<app_id>[sta_0-9]+)$',
        views.loan_requests,
        name='req_status'
),
    url(
        r'^loan_requests/(?P<app_id>[det_0-9]+)$',
        views.loan_requests,
        name='request_details'
),
    url(
        r'^workflow/$',
        views.workflow,
        name='workflow'
),
    url(
        r'^workflow/(?P<app_id>[req_0-9]+)$',
        views.workflow_request,
        name='wf_request_status'
),
    url(
        r'^workflow/(?P<app_id>[cht_0-9]+)$',
        views.workflow_request,
        name='wf_change_tier'
),
    url(
        r'^workflow/(?P<app_id>[chs_0-9]+)$',
        views.workflow_request,
        name='wf_change_status'
),
    url(
        r'^workflow/(?P<app_id>[det_0-9]+)$',
        views.workflow_request,
        name='wf_request_details'
),
    url(
        r'^loan_payments/$',
        views.loan_payments,
        name='loan_payments'
),
url(
        r'^loan_payments/(?P<loan_id>[0-9]+)$',
        views.loan_payments,
        name='make_payment'
),
    url(
        r'^loan_payments/(?P<loan_id>[vd_0-9]+)$',
        views.loan_payments,
        name='loan_details'
),
    url(
        r'^payment_history/$',
        views.payment_history,
        name='payment_history'
),
    url(
        r'^credit_verify/$',
        views.credit_verify,
        name='credit_verify'
),
     url(
        r'^certify/$',
        views.certify,
        name='certify'
),
    url(
        r'^submit_loan/$',
        views.submit_loan,
        name='submit_loan'
),
    url(
        r'^submit_loan/(?P<app_id>[c2l0-9]+)/convert$',
        ConversionWizard.as_view(
            [
                LoanTermsForm,
                WalletForm,
            ],
            template_name='dashboard/convert_to_loan.html'
        ),
        name='convert_to_loan'
),
    url(
        r'^submit_loan/(?P<app_id>[c2l0-9]+)$',
        views.submit_loan,
        name='confirm_app_info'
),
    url(
        r'^manage_loan/$',
        views.manage_loan,
        name='manage_loan'
),
    url(
        r'^loan_accounting/$',
        views.loan_accounting,
        name='loan_accounting'
),

	url(
		r'^pdf_done/(?P<app_id>[0-9]+)$',
		views.pdfgenerate,
		name='pdf_done'
),

# Form URLs

# URL to implement '+' button for Address Field
    url(
        r'^add/(?P<field_name>.+)$',
        views.new_field,
        name='add_new'
),

# url for LoanApply Wizard Form
    url(
        r'^loan_apply$', 
        LoanApplyWizard.as_view(
            [
                ContactRequestForm,
                PropertyInfoRequestForm,
                CurrentMortgageForm,
                MortgageDesiredForm,
                BorrowerInfoRequestForm
            ],
            template_name='pages/loan_apply.html'
        ), 
        name='loan_apply'
), 
    url(
        r'^loan_apply_done$', 
        TemplateView.as_view(template_name='pages/loan_apply_done.html'), 
        name='loan_apply_done'
),
# urls for BasicWizard form, as presented to the User
    url(
        r'^loan/(?P<value>[0-9]+)/basic_app/(?P<step>[0-9]+)/$',
        basic_wizard,
        name='basic_app_step'
),
    url(
        r'^loan/(?P<value>[0-9]+)/basic_app/$',
        basic_wizard,
        name='basic_app'
),
# urls for StandardWizard form, as presented to the User
    url(
        r'^loan/(?P<value>[0-9]+)/standard_app/(?P<step>.+)/$',
        standard_wizard,
        name='standard_app_step'
),
    url(
        r'^loan/(?P<value>[0-9]+)/standard_app/$',
        standard_wizard,
        name='standard_app'
),
# urls for BasicWizard form - for testing, these are the links that show in dashboard navigation
    url(
        r'^basic_app/(?P<step>.+)/$',
        basic_wizard,
        name='basic_app_step'
),
    url(
        r'^basic_app/$',
        basic_wizard,
        name='basic_app'
),
# urls for StandardWizard form - for testing, these are the links that show in dashboard navigation
    url(
        r'^standard_app/(?P<step>.+)/$',
        standard_wizard,
        name='standard_app_step'
),
    url(
        r'^standard_app/$',
        standard_wizard,
        name='standard_app'
),


# urls for ExtendedWizard - Yet to be created
#   url(
#        r'^extended_app/(?P<step>.+)/$',
#        extended_wizard,
#        name='extended_app_step'
#),
#    url(
#        r'^extended_app/$',
#        extended_wizard,
#        name='extended_app'
#),
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

