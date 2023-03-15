import debug_toolbar
from django.urls import include, path
from rest_framework import routers
from tutorial.quickstart import views

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)


# for:
# path('auth/', include('djoser.urls')),
# path('auth/', include('djoser.urls.jwt')),
# it's used for jwt in djoser

urlpatterns = [
    # path('', include(router.urls)),
    path('', include('snippets.urls')),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('__debug__/', include(debug_toolbar.urls)),
]
