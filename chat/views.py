from django.shortcuts import render
import threading
from channels.layers import get_channel_layer
# Create your views here.
def index(request):
    print("THREAD ID",threading.get_native_id())
    # channel_layer = get_channel_layer()
    # await channel_layer.group_send("chat_first",{
    #         'type': 'chat_message',
    #         'message':'notification',
    #     })
    
    return render(request, "chat/index.html")
    
def room(request, room_name):
    return render(request, "chat/room.html", {"room_name": room_name})