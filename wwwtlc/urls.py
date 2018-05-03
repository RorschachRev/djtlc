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
from loan import views as views_loan

urlpatterns = [
    url(r'^$', TemplateView.as_view(template_name = 'pages/home.html'), name='home'),
    url(r'^login/$', auth_views.login, {'template_name': 'pages/login.html'}, name='login'),
    url(r'^logout/$', auth_views.logout, {'template_name': 'pages/logout.html'}, name='logout'),
    url(r'^account.html$', views_form.account, name='account'),
    url(r'^wallet.html$', views.wallet, name='wallet'),
    url(r'^loan.html$', views.loan, name='loan'),
    url(r'^loan_apply.html$', views_loan.loan_apply, name='loan_apply'), #working url for loan_apply, it goes through the loan app's view instead of the project view
#    url(r'^loan_apply_done.html$', views.loan_apply, name='loan_apply_done'),
    url(r'^admin/', admin.site.urls),

]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

