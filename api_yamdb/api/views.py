from django.db.models import Avg
from rest_framework.generics import get_object_or_404
from rest_framework import viewsets
from reviews.models import Category, Genre, Review, Title

from .permissions import UserAuthorModeratorAdminOrReadOnly
from .serializers import (CategorySerializer, CommentSerializer,
                          GenreSerializer, ReviewSerializer, TitleSerializer)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.annotate(rating=Avg('title_reviews__score'))
    serializer_class = TitleSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (
        UserAuthorModeratorAdminOrReadOnly,
    )

    def get_title(self):
        return get_object_or_404(Title,id=self.kwargs.get('title_id'))

    def get_queryset(self):
        return self.get_title().title_reviews.all()

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user, title=self.get_title()
        )


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (
        UserAuthorModeratorAdminOrReadOnly,
    )

    def get_review(self):
        return get_object_or_404(Review,id=self.kwargs.get('review_id'))

    def get_queryset(self):
        return self.get_review().review_comments.all()

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user, review=self.get_review()
        )
