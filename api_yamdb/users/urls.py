from django.urls import include, path
from rest_framework import routers
from rest_framework.authtoken import views

from .views import UserViewSet

router = routers.DefaultRouter()

router.register(r'users', UserViewSet)

urlpatterns = [
    path('api-token-auth/', views.obtain_auth_token, name='auth-token'),
    path('', include(router.urls)),
]
