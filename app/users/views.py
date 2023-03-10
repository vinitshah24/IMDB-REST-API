from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework import status
from drf_spectacular.utils import extend_schema

from users.serializers import RegistrationSerializer
from users import models


@extend_schema(tags=['account'], description='Register a new user')
@api_view(['POST'])
def registration_view(request):
    if request.method == 'POST':
        serializer = RegistrationSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            account = serializer.save()
            token = Token.objects.get(user=account).key
            data['response'] = "Registration Successful!"
            data['username'] = account.username
            data['email'] = account.email
            data['token'] = token
        else:
            data = serializer.errors
        return Response(data, status=status.HTTP_201_CREATED)


@extend_schema(tags=['account'], description='Logout a user')
@api_view(['POST'])
def logout_view(request):
    if request.method == 'POST':
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)
