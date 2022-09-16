from django.urls import include, path
from rest_framework import routers

from .views import (CategoryViewSet, CommentViewSet, GenreViewSet,
                    ReviewViewSet, TitletViewSet)

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

urlpatterns = [
    path('v1/', include(router.urls)),
]
