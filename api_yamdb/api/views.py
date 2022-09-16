from django.shortcuts import get_object_or_404
from rest_framework import filters, viewsets
from rest_framework.pagination import PageNumberPagination
цfrom rest_framework.permissions import IsAdminUser
from reviews.models import Category, Genre, Review, Title

from .mixins import CustomViewSet
from .permissions import IsOwnerAdminModeratorOrReadOnly
from .serializers import (CategorySerializer, CommentSerializer,
                          GenreSerializer, ReviewSerializer, TitleSerializer)


class CategoryViewSet(CustomViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
#    permission_classes = (IsAdminUser,)
    pagination_class = PageNumberPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class GenreViewSet(CustomViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
#    permission_classes = (IsAdminUser,)
    pagination_class = PageNumberPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class TitletViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    pagination_class = PageNumberPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name', 'year', 'category__slug', 'genre__slug')

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
# поле рейтинг только для показа по умолчанию


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (IsOwnerAdminModeratorOrReadOnly,)
    # или на уровне проекта добавить

    def get_review(self):
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, pk=review_id)
        return review

    def get_queryset(self):
        review = self.get_review()
        queryset = review.comments.select_related('author').all()
        return queryset

    def perform_create(self, serializer):
        serializer.save(author=self.request.user,
                        post=self.get_review())


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    pagination_class = PageNumberPagination
    permission_classes = (IsOwnerAdminModeratorOrReadOnly,)
    # или на уровне проекта добавить
#    filter_backends
#    search_fields
#    filterset_fields
#    ordering_fields

    def get_title(self):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, pk=title_id)
        return title

    def get_queryset(self):
        title = self.get_title()
        queryset = title.reviews.select_related('author').all()
        return queryset

    def perform_create(self, serializer):
        serializer.save(author=self.request.user,
                        title=self.get_title())
