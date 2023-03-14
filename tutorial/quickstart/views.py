from django.contrib.auth.models import User, Group
from django.contrib.auth import get_user_model
from rest_framework import viewsets
from rest_framework import permissions
from tutorial.quickstart.serializers import UserSerializer, GroupSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    # because we custom the user model in auth_custom module
    # so we need to call get_user_model() to get the new user model
    user = get_user_model()
    queryset = user.objects.all().order_by('-date_joined')
    # normally, we just need to call User.objects.all() as below
    # queryset = User.objects.all().order_by('-date_joined')

    serializer_class = UserSerializer
    # if enable this, we will need to authenticate to use this api
    # permission_classes = [permissions.IsAuthenticated]


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    # if enable this, we will need to authenticate to use this api
    # permission_classes = [permissions.IsAuthenticated]
