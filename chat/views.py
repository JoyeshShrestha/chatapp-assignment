from django.shortcuts import render
import threading
from channels.layers import get_channel_layer
from groups.models import Groups
from rest_framework.exceptions import AuthenticationFailed
from channels.db import database_sync_to_async
from .authentication import LoginAuthentication
from .forms import RoomNameForm
from rest_framework.views import APIView
import jwt
from user_profile.models import User as CustomUser

# Create your views here.
    # authentication_classes = [LoginAuthentication]

async def index(request):
        await check_token(request)
        if request.method == 'POST':


            form = RoomNameForm(request.POST)
            if form.is_valid():
                room_name = form.cleaned_data['room_name']
                group = await get_group_by_name(room_name)
                
                print ("group is",group)

                # Do something with the room_name, e.g., save it to a database
                # authentication_classes = [LoginAuthentication]
                if group is None:
                    return render(request, 'chat/room_not_found.html', {'room_name': room_name})
                else:
                    return render(request, 'chat/room.html', {'room_name': room_name})
                    
        else:
            form = RoomNameForm()     
            
        print("THREAD ID",threading.get_native_id())
        # channel_layer = get_channel_layer()
        # await channel_layer.group_send("chat_first",{
        #         'type': 'chat_message',
        #         'message':'notification',
        #     })
        
        return render(request, "chat/index.html")
        
def room(request, room_name):
        try:
            group = get_group_by_name(room_name)
            if group is None:
                # raise AuthenticationFailed("Group not found")
                return render(request, "chat/room_not_found.html", {"room_name": "room_not_found"})
                
        except AuthenticationFailed as e:
                    # raise AuthenticationFailed("Group not found")
                return render(request, "chat/room_not_found.html", {"room_name": "room_not_found"})
        
        return render(request, "chat/room.html", {"room_name": room_name})

@database_sync_to_async
def get_group_by_name(name):
    try:
        group = Groups.objects.get(name=name)
        return group
    except:
        return None
@database_sync_to_async
def check_token(request):
    token = request.COOKIES.get('jwt')
    if not token:
            raise AuthenticationFailed('Unaunthenticated!')
            return None
    try:
            payload = jwt.decode(token, 'secret_key', algorithms=['HS256'])

        
    except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unaunthenticated!')
        
    except jwt.DecodeError as e:
            # Print or log the error message for debugging purposes
            print(f"Token decode error: {e}")
            raise AuthenticationFailed(f'Token is invalid')
        
    member = CustomUser.objects.filter(id=payload['id']).first()
        
    if member is None:
            raise AuthenticationFailed('User not found')
            