from django.test import TestCase
from django.contrib.auth.models import User
from wwwtlc.views import *
from django.test import Client
from wwwtlc import settings
from django.conf import settings
from django.test.utils import setup_test_environment
# 127.0.0.1/admin/auth/user/add/
class UserTestCase(TestCase):
	
	def setUp(self):
		setup_test_environment()
		self.user=User.objects.create_user(username='RAnD0mcRazY', email='RAnD0mcRazy@RAnD0mcRazy.com', password='RAnD0mcRazy')
		self.c=Client()

	def test_user_exist(self):
		self.assertTrue(User.objects.filter(username='RAnD0mcRazY').exists())
		
	def test_user_signup(self):
		response = c.post('/admin/auth/user/add/', {'username': 'RAnD0mcRaZy', 'password':'RAnD0mcRaZy'})
		temp=User.objects.get(username='RAnD0mcRaZy')
		Id=temp.id
		self.assertLessEqual(Id, 1024)
	def tearDown(self):
		self.user.delete()
