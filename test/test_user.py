from django.test import TestCase
from django.contrib.auth.models import User

class UserTestCase(TestCase):
	
	def setUp(self):
		self.user=User.objects.create_user(username='RAnD0mcRazY', email='RAnD0mcRazy@RAnD0mcRazy.com', password='RAnD0mcRazy')
	
	def test_user_exist(self):
		self.assertTrue(User.objects.filter(username='RAnD0mcRazY').exists())
		
	def tearDown(self):
		self.user.delete()