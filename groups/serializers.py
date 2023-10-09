from rest_framework import serializers
from .models import Groups


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Groups
        fields = '__all__'

class ViewMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Groups
        fields = ['name']

class AddMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Groups
        fields = ['members']