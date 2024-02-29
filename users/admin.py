from django.contrib import admin

from expenses.models import Balance, Expense, Passbook
from .models import User 

admin.site.register(User)
admin.site.register(Expense)
admin.site.register(Balance)
admin.site.register(Passbook)
# Register your models here.
