from django.test import TestCase
from django.contrib.auth.models import User
from wwwtlc.views import *
from django.test import Client
from wwwtlc import settings
from django.conf import settings
# 127.0.0.1/admin/auth/user/add/
class UserTestCase(TestCase):
	
	def setUp(self):
		self.user=User.objects.create_user(username='RAnD0mcRazY', email='RAnD0mcRazy@RAnD0mcRazy.com', password='RAnD0mcRazy')
		self.c=Client()
	
	def test_user_exist(self):
		self.assertTrue(User.objects.filter(username='RAnD0mcRazY').exists())
		
	def test_user_signup(self):
		response = c.post('/admin/auth/user/add/', {'username': 'RAnD0mcRaZy', 'password':'RAnD0mcRaZy'})
		
	def tearDown(self):
		self.user.delete()
