from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets
from rest_framework.pagination import PageNumberPagination
from reviews.models import Category, Genre, Review, Title

from .filtersets import TitleFilterSet
from .mixins import CustomViewSet
from .permissions import IsAdminOrReadOnly, IsOwnerAdminModeratorOrReadOnly
from .serializers import (CategorySerializer, CommentSerializer,
                          GenreSerializer, ReviewCreateSerializer,
                          ReviewSerializer, TitleCreateSerializer,
                          TitleSerializer)


class TitletViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all().order_by('year')
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    permission_classes = (IsAdminOrReadOnly,)
    pagination_class = PageNumberPagination
    filterset_class = TitleFilterSet

    def get_serializer_class(self):
        """
        Задает разные сериализаторы для создания, изменения
        и других действий
        """
        if self.request.method in ('POST', 'PATCH',):
            return TitleCreateSerializer
        return TitleSerializer


class CategoryViewSet(CustomViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ("name",)
    lookup_field = 'slug'


class GenreViewSet(CustomViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAdminOrReadOnly,)
    pagination_class = PageNumberPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name', )
    lookup_field = 'slug'


class ReviewViewSet(viewsets.ModelViewSet):
    pagination_class = PageNumberPagination
    permission_classes = (IsOwnerAdminModeratorOrReadOnly,)

    def title_obj(self):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, pk=title_id)
        return title

    def get_queryset(self):
        title = self.title_obj()
        queryset = title.reviews.select_related('author').all()
        return queryset

    def perform_create(self, serializer):
        serializer.save(author=self.request.user,
                        title=self.title_obj())

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return ReviewCreateSerializer
        return ReviewSerializer


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (IsOwnerAdminModeratorOrReadOnly,)

    def review_obj(self):
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, pk=review_id)
        return review

    def get_queryset(self):
        review = self.review_obj()
        queryset = review.comments.select_related('author').all()
        return queryset

    def perform_create(self, serializer):
        serializer.save(author=self.request.user,
                        review=self.review_obj())
