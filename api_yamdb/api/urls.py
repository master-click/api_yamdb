from rest_framework import routers
from .views import CategoryViewSet, GenreViewSet, TitleViewSet
from django.urls import include, path


router = routers.DefaultRouter()
router.register(r'v1/categories', CategoryViewSet, basename='category')
router.register(r'v1/genres', GenreViewSet, basename='genre')
router.register(r'v1/title', TitleViewSet, basename='title')

urlpatterns = [
    path('', include(router.urls)),
]
