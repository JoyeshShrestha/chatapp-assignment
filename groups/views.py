from django.shortcuts import render
from .authentication import LoginAuthentication
from .models import Groups
from .serializers import GroupSerializer, ViewMemberSerializer, AddMemberSerializer
from rest_framework.views import APIView
from rest_framework.exceptions import AuthenticationFailed, PermissionDenied
import jwt
from rest_framework.response import Response
from user_profile.models import User as CustomUser
import json

#view all the group and add a new group
class GroupView(APIView):
    authentication_classes = [LoginAuthentication]
    def get(self,request):
        allGroups=Groups.objects.all()
        serializer = GroupSerializer(allGroups,  many=True)
        return Response(serializer.data)
    
    def post(self,request):
        member = request.user
        
        serializer = GroupSerializer(data = request.data)
        serializer.is_valid(raise_exception = True)
        new_group = serializer.save()
        new_group.members.add(member)
        return Response(serializer.data)
    

#view all the groups that the user is a member of

class UGView(APIView):
    authentication_classes = [LoginAuthentication]

    def get(self, request):
       
        member = request.user
        user_id = member.id

        Allgroups =  Groups.objects.filter(members = user_id)
        serializer = ViewMemberSerializer(Allgroups, many=True)
        response = Response()
        
        
        return Response({"YourGroups": serializer.data})
        
        


#add members to the group    
class addMembersView(APIView):
    authentication_classes = [LoginAuthentication]
     
    def post(self,request):
        # token = request.COOKIES.get('jwt')
        # if not token:
        #     raise AuthenticationFailed('Unaunthenticated!')
        
        # try:
        #     payload = jwt.decode(token, 'secret_key', algorithms=['HS256'])

        
        # except jwt.ExpiredSignatureError:
        #     raise AuthenticationFailed('Unaunthenticated!')
        
        # except jwt.DecodeError as e:
        #     # Print or log the error message for debugging purposes
        #     print(f"Token decode error: {e}")
        #     raise AuthenticationFailed(f'Token is invalid')
        member_data = request.data.get('member_name', '')
        group_name = request.data.get('group_name', '')
        member = request.user
        id = member.id

        # member = User.objects.filter(id=payload['id']).first()
        
        specific_group = Groups.objects.filter(name=group_name).first()
        if not specific_group:
            raise AuthenticationFailed(f'Group not found')
        members_of_specific_group=specific_group.members.all()
        
        if id not in members_of_specific_group.values_list('id', flat=True):
            raise PermissionDenied("You are not a member of this group.")
        
       
        
        user_to_add = CustomUser.objects.filter(username=member_data).first()
        if not user_to_add:
            raise AssertionError(f'No such profile: {member_data}')

# Append the user ID to idList
        specific_group.members.add(user_to_add.id)
        
        
        
        # serializer.is_valid(raise_exception = True)
        # new_group = serializer.save()
        # new_group.name.add(group_name)
        return Response({'message': f'{member_data} added to the group successfully'})  