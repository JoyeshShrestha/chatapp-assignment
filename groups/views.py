from django.shortcuts import render
from .models import Groups
from .serializers import GroupSerializer
from rest_framework.views import APIView
from rest_framework.exceptions import AuthenticationFailed
import jwt
from rest_framework.response import Response
from user_profile.models import User
# Create your views here.
class GroupView(APIView):
    def get(self,request):
        allGroups=Groups.objects.all()
        serializer = GroupSerializer(allGroups,  many=True)
        return Response(serializer.data)
    
    def post(self,request):
        token = request.COOKIES.get('jwt')
        if not token:
            raise AuthenticationFailed('Unaunthenticated!')
        
        try:
            payload = jwt.decode(token, 'secret_key', algorithms=['HS256'])

        
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unaunthenticated!')
        
        except jwt.DecodeError as e:
            # Print or log the error message for debugging purposes
            print(f"Token decode error: {e}")
            raise AuthenticationFailed(f'Token is invalid')
        
        member = User.objects.filter(id=payload['id']).first()
        serializer = GroupSerializer(data = request.data)
        serializer.is_valid(raise_exception = True)
        new_group = serializer.save()
        new_group.members.add(member)
        return Response(serializer.data)