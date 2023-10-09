from django import forms

class RoomNameForm(forms.Form):
    room_name = forms.CharField(max_length=100)
