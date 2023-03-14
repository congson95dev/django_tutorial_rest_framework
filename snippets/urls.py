from django.urls import path, include

# we have 2 ways to use "routers"
# first way:
# this is default way of django rest framework
# from rest_framework.routers import DefaultRouter

# second way:
# this is custom way from https://github.com/alanjds/drf-nested-routers
from rest_framework_nested import routers

from rest_framework.urlpatterns import format_suffix_patterns

from snippets import views
from snippets.views import SnippetViewSet, UserViewSet

# There are 4 ways to call urlpatterns, each way serve to difference purpose.
# First way is used when snippets/views.py use "views"
# Second way, third way, fourth way is used when snippets/views.py use "viewset"

# First way:
# In first way, we need to use views.view_class_name.as_view()
# Ex: views.SnippetList.as_view()

# urlpatterns = [
#     path('', views.api_root),
#     path('snippets/', views.SnippetList.as_view(), name='snippet-list'),
#     path('snippets/<int:pk>/', views.SnippetDetail.as_view(), name='snippet-detail'),
#     path('users/', views.UserList.as_view(), name='user-list'),
#     path('users/<int:pk>/', views.UserDetail.as_view(), name='user-detail'),
# ]


# Second way:
# In second way, we need to use views.view_set_class_name.as_view({'method': 'function'})
# Ex: views.SnippetViewSet.as_view({'get': 'list', 'post': 'create'})

# We'll separate it into 2 steps:

# Step 1:
# snippet_list = SnippetViewSet.as_view({
#     'get': 'list',
#     'post': 'create'
# })
# snippet_detail = SnippetViewSet.as_view({
#     'get': 'retrieve',
#     'put': 'update',
#     'delete': 'destroy'
# })
# user_list = UserViewSet.as_view({
#     'get': 'list'
# })
# user_detail = UserViewSet.as_view({
#     'get': 'retrieve'
# })
#
# # Step 2:
# urlpatterns = format_suffix_patterns([
#     path('', views.api_root),
#     path('snippets/', snippet_list, name='snippet-list'),
#     path('snippets/<int:pk>/', snippet_detail, name='snippet-detail'),
#     path('users/', user_list, name='user-list'),
#     path('users/<int:pk>/', user_detail, name='user-detail')
# ])

# the above 2 steps equal to:

# urlpatterns = format_suffix_patterns([
#     ...
#     path('snippets/', views.SnippetViewSet.as_view({'get': 'list', 'post': 'create'}), name='snippet-list'),
#     ...
# ])


# Third way:
# In third way, we just need to call DefaultRouter(), and register url and viewset to it

# In this 3rd way, we don't need to set views.api_root for url '' as we do in 1st and 2nd ways
# Because it automatically done that for us

# We'll separate it into 2 steps:

# Step 1:
# router = DefaultRouter()
# router.register('snippets', views.SnippetViewSet)
# router.register('users', views.UserViewSet)
# router.register('snippet_tags', views.SnippetTagViewSet)

# Step 2:
# urlpatterns = router.urls

# Fourth way:
# This is updated for 3rd way, by using "nested routers"

# We'll separate it into 2 steps:

# Step 1:
# Still register router as normal as 3rd way

# "basename" is used when we set get_queryset() function in views.py
# and the logic inside that function is too complicated to django to understand and automatic render the basename
router = routers.DefaultRouter()
router.register('snippets', views.SnippetViewSet, basename='snippets')
router.register('users', views.UserViewSet, basename='users')
router.register('carts', views.CartViewSet, basename='carts')

# Register nested router
# this one will render url like:
# /snippets/<snippet_pk>/snippet_tags/
# /snippets/<snippet_pk>/snippet_tags/1
# about the "<snippet_pk>", it was rendered by "lookup"
snippets_router = routers.NestedSimpleRouter(router, 'snippets', lookup='snippet')
snippets_router.register(r'snippet_tags', views.SnippetTagViewSet, basename='snippet_tags')

carts_router = routers.NestedSimpleRouter(router, 'carts', lookup='cart')
carts_router.register(r'items', views.CartItemViewSet, basename='items')

# Step 2:
# To add all the routers to urlpatterns, we just need to plus them together
urlpatterns = router.urls + snippets_router.urls + carts_router.urls
