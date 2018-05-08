from django.contrib import admin
from .models import Person, Address, Verified, Wallet

# Register your models here.
admin.site.register(Person)
admin.site.register(Address)
admin.site.register(Verified)
admin.site.register(Wallet)
