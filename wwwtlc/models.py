import datetime
from decimal import Decimal
from django.db import models


from django.utils import timezone


class Person(models.Model):
    def __str__(self):
        return self.title

class Loan(models.Model):
    def __str__(self):
        return self.title

class Loan_Data(models.Model):
    def __str__(self):
        return self.title
