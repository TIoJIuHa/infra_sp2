from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.filters import SearchFilter
from reviews.models import Category, Genre, Review, Title

from .filters import TitleFilter
from .mixins import ListDestroyCreateViewSet
from .permissions import (
    IsAdminOrReadOnly,
    IsAuthorOrReadOnly,
    IsModeratorOrReadOnly,
)
from .serializers import (
    CategorySerializer,
    CommentSerializer,
    GenreSerializer,
    ReviewSerializer,
    TitleSerializer,
    TitlePostSerialzier
)


class CategoryViewSet(ListDestroyCreateViewSet):
    """
    Вьюсет для модели Категории.
    Делать запрос может любой, редактировать и удалять - только админ.
    """

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (SearchFilter,)
    search_fields = ("name",)
    lookup_field = "slug"


class GenreViewSet(ListDestroyCreateViewSet):
    """
    Вьюсет для модели Жанры.
    Делать запрос может любой, редактировать и удалять - только админ
    """

    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (SearchFilter,)
    search_fields = ("name",)
    lookup_field = "slug"


class TitleViewSet(viewsets.ModelViewSet):
    """
    Вьюсет для модели Произведения.
    Делать запрос может любой, редактировать и удалять - только админ.
    """

    queryset = Title.objects.annotate(rating=Avg("reviews__score"))
    serializer_class = TitleSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.request.method in ['POST', 'PUT', 'PATCH']:
            return TitlePostSerialzier
        return TitleSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    """
    Вьюсет для модели отзыва.
    Делать запрос может любой, добавлять только аутентифицированный.
    Редактировать и удалять только автор, модератор или админ.
    """

    serializer_class = ReviewSerializer
    permission_classes = (
        IsAuthorOrReadOnly | IsModeratorOrReadOnly | IsAdminOrReadOnly,
    )

    def get_title(self):
        title = get_object_or_404(Title, id=self.kwargs.get("title_id"))
        return title

    def perform_create(self, serializer):
        title = self.get_title()
        serializer.save(author=self.request.user, title=title)

    def get_queryset(self):
        title = self.get_title()
        return title.reviews.all()


class CommentViewSet(viewsets.ModelViewSet):
    """
    Вьюсет для модели комментария.
    Делать запрос может любой, добавлять только аутентифицированный.
    Редактировать и удалять только автор, модератор или админ.
    """

    serializer_class = CommentSerializer
    permission_classes = (
        IsAuthorOrReadOnly | IsModeratorOrReadOnly | IsAdminOrReadOnly,
    )

    def get_review(self):
        review = get_object_or_404(
            Review,
            id=self.kwargs.get("review_id"),
        )
        return review

    def perform_create(self, serializer):
        review = self.get_review()
        serializer.save(author=self.request.user, review=review)

    def get_queryset(self):
        review = self.get_review()
        return review.comments.all()
