from rest_framework import routers
from .views import CategoryViewSet, GenreViewSet, TitleViewSet
from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .views import (UsersViewSet, signup, get_token)


router = routers.DefaultRouter()
router.register(r'v1/categories', CategoryViewSet, basename='category')
router.register(r'v1/genres', GenreViewSet, basename='genre')
router.register(r'v1/title', TitleViewSet, basename='title')

urlpatterns = [
    path('', include(router.urls)),


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
