from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.urlpatterns import format_suffix_patterns

from snippets import views
from snippets.views import SnippetViewSet, UserViewSet

# There are 2 ways to call urlpatterns, each way serve to difference purpose.
# First way is used when snippets/views.py use "views"
# Second way is used when snippets/views.py use "viewset"
# In first way, we need to use views.view_class_name.as_view()
# In second way, we need to use views.view_set_class_name.as_view({'method': 'function'})

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
snippet_list = SnippetViewSet.as_view({
    'get': 'list',
    'post': 'create'
})
snippet_detail = SnippetViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'delete': 'destroy'
})
user_list = UserViewSet.as_view({
    'get': 'list'
})
user_detail = UserViewSet.as_view({
    'get': 'retrieve'
})

# Step 2:
urlpatterns = format_suffix_patterns([
    path('', views.api_root),
    path('snippets/', snippet_list, name='snippet-list'),
    path('snippets/<int:pk>/', snippet_detail, name='snippet-detail'),
    path('users/', user_list, name='user-list'),
    path('users/<int:pk>/', user_detail, name='user-detail')
])

# the above 2 steps equal to:

# urlpatterns = format_suffix_patterns([
#     ...
#     path('snippets/', views.SnippetViewSet.as_view({'get': 'list', 'post': 'create'}), name='snippet-list'),
#     ...
# ])


