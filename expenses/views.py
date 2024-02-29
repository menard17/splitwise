from decimal import Decimal
import json
from django.shortcuts import render
from expenses.models import Balance, Expense, Passbook
from users import serializers
from users.models import User
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from django.db import transaction
from django.core.serializers.json import DjangoJSONEncoder
from django.core.serializers import serialize

# Create your views here.
@csrf_exempt
def add_expense(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        payer_user = data['payer_user']
        amount = data['totalAmount']
        expense_type = data['splitType']
        description = data.get('description', '')
        participants = data['participants']
        shares = data.get('shares', [])

        payer = get_object_or_404(User, name=payer_user)
        balances = []
        with transaction.atomic():
            expense = Expense.objects.create(
                paid_by=payer,
                total_amount=amount,
                expense_type=expense_type,
                shares = shares,
                description=description,)
            expense.participants.set(participants)
            for i, participant in enumerate(expense.participants.all()):
                if len(expense.shares) > 1:
                    share = expense.shares.split()[i]
                else:
                    share = 0
                cal_amount = calculate_amount_owed(amount, expense_type, share, len(expense.participants.all()))

                balance, created = Balance.objects.get_or_create(
                    user=expense.paid_by,
                    friend=participant,
                )
                balance.amount += Decimal(cal_amount)
                balance.save()
                balance_data = {'user_name': participant.name, 'balance': balance.amount}
                balances.append(balance_data)
            print("=====test=====")
            print(balances)
            Passbook.objects.create(
                user=payer,
                amount=expense.total_amount,
                date=expense.created_at,
                description=expense.description,
                share_type=expense_type,
                participants=participants,
                balances=json.dumps(balances, cls=DjangoJSONEncoder)
            )
        return JsonResponse({'status': 'success', 'message': 'Expense added successfully'})
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid HTTP method'})

def calculate_amount_owed(amount, expense_type, share, participants):
    if expense_type == 'EQUAL':
        return amount / participants
    elif expense_type == 'EXACT':
        return share
    elif expense_type == 'PERCENT':
        return (int(share) / 100) * amount

def get_user_balances(request, user_id):
    try:
        user = User.objects.get(userId=user_id)
    except User.DoesNotExist:
        return JsonResponse({'error': 'User not found'}, status=404)

    all_users = User.objects.exclude(userId=user_id)
    balances = {}

    for other_user in all_users:
        user_balance = calculate_user_balance(user, other_user)
        balances[other_user.userId] = {'user_name': other_user.name, 'balance': user_balance}

    response_data = {
        'user_id': user.userId,
        'balances': balances,
    }
    return JsonResponse(response_data, safe=False)

def calculate_user_balance(user, with_user):
    user_balance = Balance.objects.filter(user=user, friend=with_user)
    return user_balance.values('amount')[0]['amount'] if user_balance else 0

def get_user_passbook(request, user_id):
    try:
        user = User.objects.get(userId=user_id)
    except User.DoesNotExist:
        return JsonResponse({'error': 'User not found'}, status=404)


    passbook_book = Passbook.objects.filter(user=user)
    json_data = serialize('json', passbook_book)

    response_data = {
        'user_id': user.userId,
        'passbook_book': json_data,
    }
    return JsonResponse(response_data, safe=False)