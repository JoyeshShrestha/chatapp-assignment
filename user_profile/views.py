from django.shortcuts import render
from rest_framework import status

from .models import User
from rest_framework.views import APIView
import secrets
from .serializers import UserSerializer
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
import jwt, datetime

class RegisterView(APIView):
    # class RegisterView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            response_data = {
                'username': user.username,
                'email': user.email,
                'password': user.password,
            }
            return Response(response_data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    # def post(self,request):
        User.objects.create()
        serializer = UserSerializer(data = request.data)
        serializer.is_valid(raise_exception = True)
        serializer.save()
        return Response(serializer.data)

# Create your views here.
class LoginView(APIView):
    def post(self,request):
        email = request.data['email']
        password = request.data['password']

        user = User.objects.filter(email=email).first()

        if user is None:
            raise AuthenticationFailed('User not found!')
        
        if not user.check_password(password):
            raise AuthenticationFailed('Incorrect password!')
        
        payload = {
            'id' : user.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes = 60),
            'iat': datetime.datetime.utcnow()
        }
        

        token = jwt.encode(payload, 'secret_key', algorithm = 'HS256')
        decoded_payload = jwt.decode(token, 'secret_key', algorithms=['HS256'])
        
        response = Response()


        response.set_cookie(key='jwt', value=token, httponly=True)
        response.data = {
                        'message' : token

        }
        
        
         
        
        
        return response