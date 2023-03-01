from django.contrib.auth.models import User
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status, mixins, generics, permissions, renderers, viewsets
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.views import APIView

from snippets.models import Snippet
from snippets.permissions import IsOwnerOrReadOnly
from snippets.serializers import SnippetSerializer, UserSerializer


# override the home page list api
# we'll call this later in snippets/urls.py with "/"
# remember to check file tutorial/urls.py to see if they have define for url "/" or not
# if they do, remove or comment it so it won't override us
# after we setup successfully, try to run to homepage, ex: 128.0.0.1:8000/
# we will see the suggestion there.
@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'users': reverse('user-list', request=request, format=format),
        'snippets': reverse('snippet-list', request=request, format=format)
    })


# ======================================================================================================================

# There are 5 ways to do CRUD in django
# The 1st, 2nd, 3rd, 4th ways is the best practice, the 5th way not so much,
# the 5th way just show us how django CRUD could be done in that way
# The 1st way is come from https://www.django-rest-framework.org/tutorial/6-viewsets-and-routers/
# The 2nd, 3rd, 4th ways is come from https://www.django-rest-framework.org/tutorial/3-class-based-views/


# First way: use viewsets
# This way is the shortest way
# It combine "list" and "detail" in the 2nd way as one and call it "viewset".
class SnippetViewSet(viewsets.ModelViewSet):
    queryset = Snippet.objects.select_related('category').all()
    serializer_class = SnippetSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly]

    # this is for permission purpose
    # we do this to allow only the creator of a snippet may update or delete it.
    # https://www.django-rest-framework.org/tutorial/4-authentication-and-permissions/
    # but in this tutorial, they use perform_create, but seem like it doesn't work
    # so i follow this instruction:
    # https://stackoverflow.com/a/53172106/8962929
    # note: this method only work for 1st and 2nd solution
    def create(self, request, *args, **kwargs):
        # update column "owner" as current user
        request.data.update({'owner': request.user.id})
        return super(SnippetViewSet, self).create(request, *args, **kwargs)

    # i've already update "owner" column to snippets in create() function
    # but it's still need to do this in update() function as well
    # else, it will throw error `"owner" is required field`
    def update(self, request, *args, **kwargs):
        # update column "owner" to current user
        request.data.update({'owner': request.user.id})
        return super(SnippetViewSet, self).update(request, *args, **kwargs)


# Second way: use generics
# This way is the shortest way just after 1st way
# We can use "generics" class to make basic CRUD
# But because it's the short way, so it can only work for basic CRUD, it's not good for customization tasks
# Format to use this is by generics.className
# There are 5 className, which is "List", "Create", "Retrieve", "Update", "Destroy"
# We can combine them together
# Ex: generics.ListCreateAPIView, generics.RetrieveUpdateDestroyAPIView

# class SnippetList(generics.ListCreateAPIView):
#     # set permission
#     permission_classes = [permissions.IsAuthenticatedOrReadOnly]
#     # use queryset to access to model and get all data
#     queryset = Snippet.objects.all()
#     # use serializer_class to call serializer
#     serializer_class = SnippetSerializer
#
#     # this is for permission purpose
#     # we do this to allow only the creator of a snippet may update or delete it.
#     # https://www.django-rest-framework.org/tutorial/4-authentication-and-permissions/
#     # but in this tutorial, they use perform_create, but seem like it doesn't work
#     # so i follow this instruction:
#     # https://stackoverflow.com/a/53172106/8962929
#     # note: this method only work for 1st solution
#     def create(self, request, *args, **kwargs):
#         # update column "owner" as current user
#         request.data.update({'owner': request.user.id})
#         return super(SnippetList, self).create(request, *args, **kwargs)
#
#
# class SnippetDetail(generics.RetrieveUpdateDestroyAPIView):
#     # set permission
#     permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
#     # use queryset to access to model and get all data
#     queryset = Snippet.objects.all()
#     # use serializer_class to call serializer
#     serializer_class = SnippetSerializer
#
#     # i've already update "owner" column to snippets in create() function
#     # but it's still need to do this in update() function as well
#     # else, it will throw error `"owner" is required field`
#     def update(self, request, *args, **kwargs):
#         # update column "owner" to current user
#         request.data.update({'owner': request.user.id})
#         return super(SnippetDetail, self).update(request, *args, **kwargs)


# Third way: use mixins and generics
# This is also a short way
# With this , we can make basic CRUD
# But because it's the short way, so it can only work for basic CRUD, it's not good for customization tasks
# By using mixins, for "get list" API, rest framework will automatically format the response for us
# Format to use this is by mixins.className + generics.GenericAPIView
# There are 5 className, which is "List", "Create", "Retrieve", "Update", "Destroy"
# Not like first way, in this 2nd way, we can't combine className together
# And we need to call them separately
# ex: mixins.ListModelMixin, mixins.CreateModelMixin

# class SnippetList(mixins.ListModelMixin,
#                   mixins.CreateModelMixin,
#                   generics.GenericAPIView):
#     # use queryset to access to model and get all data
#     queryset = Snippet.objects.all()
#     # use serializer_class to call serializer
#     serializer_class = SnippetSerializer
#
#     def get(self, request, *args, **kwargs):
#         return self.list(request, *args, **kwargs)
#
#     def post(self, request, *args, **kwargs):
#         return self.create(request, *args, **kwargs)
#
#
# class SnippetDetail(mixins.RetrieveModelMixin,
#                     mixins.UpdateModelMixin,
#                     mixins.DestroyModelMixin,
#                     generics.GenericAPIView):
#     # use queryset to access to model and get all data
#     queryset = Snippet.objects.all()
#     # use serializer_class to call serializer
#     serializer_class = SnippetSerializer
#
#     def get(self, request, *args, **kwargs):
#         return self.retrieve(request, *args, **kwargs)
#
#     def put(self, request, *args, **kwargs):
#         return self.update(request, *args, **kwargs)
#
#     def delete(self, request, *args, **kwargs):
#         return self.destroy(request, *args, **kwargs)


# Forth way:
# This is the customizable way
# With this, we can customize whatever we want
# And it's not automatic save for us as 3 ways above

# class SnippetList(APIView):
#     """
#     List all snippets, or create a new snippet.
#     """
#     def get(self, request):
#         snippets = Snippet.objects.all()
#         serializer = SnippetSerializer(snippets, many=True)
#         return Response(serializer.data)
#
#     def post(self, request):
#         serializer = SnippetSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#
# class SnippetDetail(APIView):
#     """
#     Retrieve, update or delete a snippet instance.
#     """
#     def get_object(self, pk):
#         try:
#             return Snippet.objects.get(pk=pk)
#         except Snippet.DoesNotExist:
#             return Response(status=status.HTTP_404_NOT_FOUND)
#
#     def get(self, request, pk):
#         snippet = self.get_object(pk)
#         serializer = SnippetSerializer(snippet)
#         return Response(serializer.data)
#
#     def put(self, request, pk):
#         snippet = self.get_object(pk)
#         serializer = SnippetSerializer(snippet, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     def delete(self, request, pk):
#         snippet = self.get_object(pk)
#         snippet.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)


# Fifth way:
# This way is just to show us how django CRUD could be done in this way
# @api_view(['GET', 'POST'])
# # this @csrf_exempt is for ignore the csrf token in POST method, because we don't have csrf token in client
# @csrf_exempt
# def snippet_list(request):
#     """
#     List all code snippets, or create a new snippet.
#     """
#     if request.method == 'GET':
#         snippets = Snippet.objects.all()
#         serializer = SnippetSerializer(snippets, many=True)
#         return Response(serializer.data)
#
#     elif request.method == 'POST':
#         serializer = SnippetSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#
# @api_view(['GET', 'PUT', 'DELETE'])
# # this @csrf_exempt is for ignore the csrf token in POST method, because we don't have csrf token in client
# @csrf_exempt
# def snippet_detail(request, pk):
#     """
#     Retrieve, update or delete a code snippet.
#     """
#     try:
#         snippet = Snippet.objects.get(pk=pk)
#     except Snippet.DoesNotExist:
#         return Response(status=status.HTTP_404_NOT_FOUND)
#
#     if request.method == 'GET':
#         serializer = SnippetSerializer(snippet)
#         return Response(serializer.data)
#
#     elif request.method == 'PUT':
#         serializer = SnippetSerializer(snippet, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     elif request.method == 'DELETE':
#         snippet.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)

# ======================================================================================================================

# we've also set "user" to use CRUD by 1st and 2nd way as above

# 1st way:
# use viewsets
class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


# 2nd way
# use generics
# class UserList(generics.ListAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer
#
#
# class UserDetail(generics.RetrieveAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer



