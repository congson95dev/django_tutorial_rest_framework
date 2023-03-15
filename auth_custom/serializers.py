from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer, UserSerializer as BaseUserSerializer
from rest_framework import serializers

from auth_custom.models import UserProfile


# custom fields for user_create action of djoser
# after this, we also need to setting for 'user_create' action in file settings.py
class UserCreateSerializer(BaseUserCreateSerializer):
    class Meta(BaseUserCreateSerializer.Meta):
        # in default, djoser only show 3 fields when create new user
        # which is email, username, password
        # but with this, we've added more fields for it
        fields = ['email', 'username', 'password', 'first_name', 'last_name']


# custom fields for current_user action of djoser
# after this, we also need to setting for 'current_user' action in file settings.py
class UserSerializer(BaseUserSerializer):
    class Meta(BaseUserSerializer.Meta):
        # in default, djoser only show 3 fields when create new user
        # which is email, username, id
        # but with this, we've added more fields for it
        fields = ['email', 'username', 'id', 'first_name', 'last_name']


# serializers for Customers (this is custom feature, not related to djoser)
class UserProfileSerializer(serializers.ModelSerializer):

    user_id = serializers.IntegerField(read_only=True)

    class Meta:
        model = UserProfile
        fields = ['id', 'user_id', 'phone', 'birth_date', 'membership']
