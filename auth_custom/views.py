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
    # for "detail=False", it's for non pk required, if "detail=True", then in the url, we will transfer pk,
    # also we will define me() like this:
    # def me(self, request, pk)
    @action(detail=False, methods=['GET', 'PUT'])
    def me(self, request):

        # the function get_or_create() is return a turple with 2 values (user_profile and created),
        # so we need to unzip it before used it

        # also, we can prevent this by using signals to automatically create user profile whenever user is created
        # so it will never have case which is user exist but user profile isn't
        (user_profile, created) = UserProfile.objects.get_or_create(user_id=request.user.id)

        if request.method == 'GET':
            serializer = UserProfileSerializer(user_profile)
        elif request.method == 'PUT':
            serializer = UserProfileSerializer(user_profile, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
        return Response(serializer.data)
