from django.db import models

from users.models import User

# Create your models here.
class Expense(models.Model):
    EQUAL = 'EQUAL'
    EXACT = 'EXACT'
    PERCENT = 'PERCENT'

    EXPENSE_TYPES = [
        (EQUAL, 'Equal'),
        (EXACT, 'Exact'),
        (PERCENT, 'Percentage'),
    ]

    paid_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='expenses_paid')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    expense_type = models.CharField(max_length=10, choices=EXPENSE_TYPES)
    description = models.CharField(max_length=255, blank=True, null=True)
    participants = models.ManyToManyField(User, related_name='expenses_participated')
    shares = models.TextField(blank=True, null=True)  # JSON field to store shares (amount or percentages)
    created_at = models.DateTimeField(auto_now_add=True)

class Balance(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='balances')
    friend = models.ForeignKey(User, on_delete=models.CASCADE, related_name='friend_balances')
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)

class Passbook(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='passbook_entries')
    date = models.DateField()
    description = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    participants = models.JSONField()
    share_type = models.CharField(max_length=10)
    balances = models.JSONField()