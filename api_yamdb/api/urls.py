from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .views import (UsersViewSet, signup, get_token)

router_v1 = SimpleRouter()

router_v1.register(r'users', UsersViewSet)

auth_patterns = [
    path('signup/', signup),
    path('token/', get_token),
    path('', include('djoser.urls')),
    path('', include('djoser.urls.jwt')),
]

urlpatterns = [
    path('v1/auth/', include(auth_patterns)),
    path('v1/', include(router_v1.urls)),
]
