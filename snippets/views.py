from decimal import Decimal

from django.contrib.auth.models import User
from django.db.models import Count, F, Sum, ExpressionWrapper, Value
from django.forms import DecimalField
from django.http import HttpResponse, JsonResponse, QueryDict
from django.views.decorators.csrf import csrf_exempt
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, mixins, generics, permissions, renderers, viewsets
from rest_framework.decorators import api_view
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet

from snippets.filters import SnippetFilter
from snippets.models import Snippet, SnippetTag, Cart, CartItem
from snippets.pagination import CustomPagination
from snippets.permissions import IsOwnerOrReadOnly
from snippets.serializers import SnippetSerializer, UserSerializer, SnippetTagSerializer, CartSerializer, \
    CartItemSerializer, CartItemCRDSerializer, UpdateCartItemSerializer


# override the home page list api
# we'll call this later in snippets/urls.py with "/"
# remember to check file tutorial/urls.py to see if they have define for url "/" or not
# if they do, remove or comment it so it won't override us
# after we setup successfully, try to run to homepage, ex: 128.0.0.1:8000/
# we will see the suggestion there.
@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        # 'users': reverse('user-list', request=request, format=format),
        'snippets': reverse('snippet-list', request=request, format=format)
    })


# ======================================================================================================================

# There are 5 ways to do CRUD in django
# The 1st, 2nd, 3rd, 4th ways is the best practice, the 5th way not so much,
# the 5th way just show us how django CRUD could be done in that way
# The 1st way is come from https://www.django-rest-framework.org/tutorial/6-viewsets-and-routers/
# The 2nd, 3rd, 4th ways is come from https://www.django-rest-framework.org/tutorial/3-class-based-views/

# Also, for the 1st and 2nd ways, which is using generics view,
# when we come to browser, we will see in the bottom, there's a POST form
# so we can create/edit, also it provided us sample field as well


# First way: use viewsets
# This way is the shortest way
# It combine "list" and "detail" in the 2nd way as one and call it "viewset".
class SnippetViewSet(viewsets.ModelViewSet):
    queryset = Snippet.objects.select_related('category').annotate(tag_count=Count('snippet_tags')).all()
    serializer_class = SnippetSerializer

    # the generic view / viewsets expect the url config that we set in snippets/urls.py are used "pk" instead of "id"
    # to ignore that and still use "id", we can set lookup_field = "id"
    # Ex:
    # lookup_field = 'id'

    permission_classes = [permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly]

    # custom filter by using https://django-filter.readthedocs.io/en/stable/guide/usage.html
    # this library will help us lower the code for the filter
    # we can check this by open swagger and go to /snippets
    # then click to button "filter" and try to filter

    # to use custom filter, we need 2 step:
    # step 1: set DjangoFilterBackend to filter_backends
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]

    # step 2:
    # call to SnippetFilter in file snippets/filters.py
    filterset_class = SnippetFilter

    # search feature:
    # we need 2 step to setup this search feature
    # step 1:
    # set SearchFilter to filter_backends, we've already done that in above code
    # step 2:
    # set fields to search feature
    search_fields = ['title', 'code', 'category__title']
    # we can check this by open swagger and go to /snippets
    # then click to button "filter" and try to filter
    # url will be like this: snippets/?search=cat+2+zoo

    # ordering feature:
    # we need 2 step to setup this ordering feature
    # step 1:
    # set OrderingFilter to filter_backends, we've already done that in above code
    # step 2:
    # set fields to ordering feature
    ordering_fields = ['unit_price', 'created']
    # we can check this by open swagger and go to /snippets
    # then click to button "filter" and try to filter
    # url will be like this: snippets/?ordering=-unit_price,-created

    # custom pagination feature:
    # we can simply set pagination in tutorial/settings.py
    # but in some case, we will need to custom pagination for each url separately
    # such as in snippets list, the page_size = 10, but in snippet category list, the page_size = 15
    pagination_class = CustomPagination

    # we can set "queryset" by using get_queryset() function too
    # this is used when you have complicated queryset for multiple cases
    # normally, we just need to set queryset by above solution
    # def get_queryset(self):
    #     queryset = Snippet.objects.select_related('category').annotate(tag_count=Count('snippet_tags')).all()
    #     category_id = self.request.query_params.get('category_id')
    #     if category_id is not None:
    #         queryset = queryset.filter(category_id=category_id)
    #     return queryset

    # we can set "serializer_class" by using get_serializer_class() function too
    # this is used when you have complicated queryset for multiple cases
    # normally, we just need to set queryset by above solution
    # def get_serializer_class(self):
    #     return SnippetSerializer

    # this is for permission purpose
    # we do this to allow only the creator of a snippet may update or delete it.
    # https://www.django-rest-framework.org/tutorial/4-authentication-and-permissions/
    # but in this tutorial, they use perform_create, but seem like it doesn't work
    # so i follow this instruction:
    # https://stackoverflow.com/a/53172106/8962929
    # note: this method only work for 1st and 2nd solution
    def create(self, request, *args, **kwargs):
        # when we send post request from the swagger
        # the data will automatic convert to QueryDict, which is un-editable (which they called immutable)
        # so we need to check and convert it to editable (which they called mutable)
        if isinstance(request.data, QueryDict):
            _mutable = request.data._mutable
            request.data._mutable = True
            # update column "owner" as current user
            request.data['owner'] = request.user.id
            request.data._mutable = _mutable
        else:
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


# viewset for "snippet tag"
class SnippetTagViewSet(viewsets.ModelViewSet):
    serializer_class = SnippetTagSerializer

    # filter snippet tags by snippet id
    # Ex we have this url: /snippets/2/snippet_tags/
    # this url is following by format: /snippets/<snippet_pk>/snippet_tags/
    # this format is defined in snippets/urls.py
    # we will get the "snippet_pk" params by self.kwargs['snippet_pk']
    # and use that to filter
    def get_queryset(self):
        return SnippetTag.objects.filter(snippet_id=self.kwargs['snippet_pk'])

    # set data to context in serializer
    # so we can use that later
    def get_serializer_context(self):
        return {'snippet_id': self.kwargs['snippet_pk']}


class CartViewSet(mixins.CreateModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.DestroyModelMixin,
                  GenericViewSet):

    serializer_class = CartSerializer

    def get_queryset(self):
        # get unit_price and quantity
        cart_items = CartItem.objects.select_related('snippet')\
            .filter(cart_id=self.kwargs['pk'])\
            .values('snippet__unit_price', 'quantity')

        # calculate total_price
        # total_price = 0
        # for cart_item in cart_items:
        #     total_price += cart_item.get('snippet__unit_price') * cart_item.get('quantity')

        # shorter way to calculate total_price
        total_price = sum([
            cart_item.get('quantity') * cart_item.get('snippet__unit_price')
            for cart_item in cart_items
        ])

        # or we can calculate total_price by serializer for even shorter

        return Cart.objects\
            .prefetch_related('items__snippet')\
            .annotate(total_price=Value(total_price))\
            .all()


class CartItemViewSet(viewsets.ModelViewSet):
    def get_serializer_class(self):
        # we use 2 difference serializer for PUT and other method such as POST, GET
        if self.request.method == 'PUT':
            return UpdateCartItemSerializer
        return CartItemCRDSerializer

    def get_queryset(self):
        return CartItem.objects.filter(cart_id=self.kwargs['cart_pk']) 

    # set data to context in serializer
    # so we can use that later
    def get_serializer_context(self):
        return {'cart_id': self.kwargs['cart_pk']}
