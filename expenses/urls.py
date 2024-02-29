# users/urls.py
from django.urls import path
from expenses import views

urlpatterns = [
    path('expense/', views.add_expense, name='add_expense'),
    path('get_user_balances/<int:user_id>/', views.get_user_balances, name='get_user_balances'),
    path('get_user_passbook/<int:user_id>/', views.get_user_passbook, name='get_user_passbook'),
]
