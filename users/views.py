from http.client import responses
from urllib import request, response
from django.shortcuts import render
import json
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from users.models import User
from django.http import HttpResponse, JsonResponse
from users.serializers import UserSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view

@api_view(['POST'])
@csrf_exempt
def create_user(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        user = UserSerializer(data=data)
        if user.is_valid():
            user.save()
            return JsonResponse({'status': 'created successfully'})
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)

@api_view(['GET'])
@csrf_exempt
def get_users(request):
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)