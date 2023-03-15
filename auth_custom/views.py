from rest_framework import mixins
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from auth_custom.models import UserProfile
from auth_custom.serializers import UserProfileSerializer


class UserProfileViewSet(mixins.CreateModelMixin,
                         mixins.RetrieveModelMixin,
                         mixins.UpdateModelMixin,
                         GenericViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer

    # get or update current user profile
    @action(detail=False, methods=['GET', 'PUT'])
    def me(self, request):
        # the function get_or_create() is return a turple with 2 values (user_profile and created),
        # so we need to unzip it before used it
        (user_profile, created) = UserProfile.objects.get_or_create(user_id=request.user.id)
        if request.method == 'GET':
            serializer = UserProfileSerializer(user_profile)
        elif request.method == 'PUT':
            serializer = UserProfileSerializer(user_profile, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
        return Response(serializer.data)
