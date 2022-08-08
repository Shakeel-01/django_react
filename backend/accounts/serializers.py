from rest_framework import serializers
from .models import *
from datetime import datetime, timedelta, timezone
from django.db.models import Q
from djoser.serializers import UserCreateSerializer
from django.contrib.auth import get_user_model
User = get_user_model()
time_threshold = datetime.now(timezone.utc) - timedelta(minutes = 5)

class UserCreateSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = (
            'id', 
            'email', 
            'username', 
            'first_name', 
            'last_name', 
            'picture',
            'bio',
            'about',
            'role',
            'is_online',
            'is_admin', 
            'password'
        )


class UserAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAccount
        fields = '__all__'

class OnlineStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = OnlineStatus
        fields = '__all__'