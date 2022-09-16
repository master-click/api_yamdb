from django.urls import include, path
from rest_framework import routers

from .views import (CategoryViewSet, CommentViewSet, GenreViewSet,
                    ReviewViewSet, TitletViewSet)

from rest_framework.routers import SimpleRouter

from .views import (UsersViewSet, signup, get_token)


router = routers.DefaultRouter()


router.register(r'titles', TitletViewSet)
router.register(r'categories', CategoryViewSet)
router.register(r'genres', GenreViewSet)
router.register(
    r'titles\/(?P<title_id>\d+)\/reviews',
    ReviewViewSet,
    basename='title-reviews'
)
router.register(
    r'titles\/(?P<title_id>\d+)\/reviews\/(?P<review_id>\d+)\/comments',
    CommentViewSet,
    basename='review-comments'
)


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
    path('v1/', include(router.urls)),
]
