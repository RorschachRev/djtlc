#run with ../manage.py test
from django.test import TestCase
from django.contrib.auth.models import User
from wwwtlc.views import *
from django.test import Client
from wwwtlc import settings
from django.conf import settings
from django.test.utils import setup_test_environment
from wwwtlc import forms
from django.test.client import RequestFactory
# 127.0.0.1/admin/auth/user/add/
class UserTestCase(TestCase):
	
	def setUp(self):
		#~ setup_test_environment()
		self.c=Client()
		self.factory=RequestFactory()
		self.password='test0190'
		self.my_admin=User.objects.create_user('CrAzYaDmIn', 'CrAzYaDmIn@crazy.com',self.password)
		self.my_admin.is_staff=True
		self.my_admin.is_superuser=True
		self.my_admin.save()
		
	def test_user_signup(self):
		#~ pass
		#~ https://github.com/django/django/blob/master/tests/forms_tests/tests/test_validators.py
		
		#Contains user signup page basically. Should mimic their test to start, and then switch to checking the UID after getting the basic test working
		#~ https://github.com/django/django/blob/master/tests/forms_tests/widget_tests/test_passwordinput.py
		self.c.get('/signup/')
		userdata={'username':'RaNDoMcRaZy', 'password1':'TeSt1009', 'password2':'TeSt1009'}
		request=self.c.post('/signup/', userdata)
		#~ signup(request)
		u=User.objects.filter(username='RaNDoMcRaZy')
		id=u.get().id
		self.assertGreaterEqual(id, 1025)
		
	def test_manual_create(self):
		#example for admin is https://github.com/django/django/blob/master/tests/modeladmin/tests.py
		temp=User.objects.create_user('RaNDoMcRaZy', 'TeSt1009@crazy.com','TeSt1009')
		u=User.objects.filter(username='RaNDoMcRaZy')
		id=u.get().id
		self.assertLessEqual(id, 1024)
	def test_admin_page(self):
		self.factory.user=self.my_admin
		result=self.factory.get('/admin/auth/user/add')
		result.user=self.my_admin
		userdata={'username':'RaNDoMcRaZy', 'password1':'TeSt1009', 'password2':'TeSt1009'}
		self.result2=self.factory.post('/admin/auth/user/add', userdata)
		u=User.objects.filter(username='RaNDoMcRaZy')
		id=u.get().id
		self.assertLessEqual(id, 1024)
	def tearDown(self):
		pass
		#~ teardown_test_environment()
