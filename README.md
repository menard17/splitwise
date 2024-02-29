HOW TO RUN?
python manage.py migrate
python manage.py runserver

API Contracts:

1. Add User:
Endpoint: POST /users/create/
Request:
json
{
    "name": "User4",
    "email": "tes@gmail.com",
    "mobile": 122565
}

2. Add Expense (Percentage):
Endpoint: POST api/expense/
Request:
json
{
    "payer_user": "User1",
    "name": "Electricity Bill",
    "totalAmount": 1000,
    "participants": [
        "1",
        "2",
        "3",
        "4"
    ],
    "splitType": "PERCENT",
    "shares": "40 20 20 20"
}
Response:
json
{
  "status": "success",
  "message": "Expense added successfully"
}
4. Show Balances:
Endpoint: GET /api/get_user_balances/<user_id>
Response:
json
{
    "user_id": 1,
    "balances": {
        "2": {
            "user_name": "User2",
            "balance": "850.00"
        },
        "3": {
            "user_name": "User3",
            "balance": "850.00"
        },
        "4": {
            "user_name": "User4",
            "balance": "850.00"
        }
    }
}
6. Show Passbook:
Endpoint: GET /api/get_user_passbook/<user_id>
Response:
json
{
    "user_id": 1,
    "passbook_book": "[{\"model\": \"expenses.passbook\", \"pk\": 1, \"fields\": {\"user\": 1, \"date\": \"2024-02-29\", \"description\": \"\", \"amount\": \"1000.00\", \"participants\": [\"1\", \"2\", \"3\", \"4\"], \"share_type\": \"PERCENT\", \"balances\": \"[{\\\"user_name\\\": \\\"User1\\\", \\\"balance\\\": \\\"2250.00\\\"}, {\\\"user_name\\\": \\\"User2\\\", \\\"balance\\\": \\\"1450.00\\\"}, {\\\"user_name\\\": \\\"User3\\\", \\\"balance\\\": \\\"1450.00\\\"}, {\\\"user_name\\\": \\\"User4\\\", \\\"balance\\\": \\\"1450.00\\\"}]\"}}]"
}