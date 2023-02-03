from api_yamdb.settings import DEFAULT_FROM_EMAIL
from core.filters import TitleFilter
from core.permissions import (IsAdmin, IsAdminOrReadOnly,
                              UserAdminModeratorOrReadOnly)
from core.viewsets import GetPostDeleteViewSet
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.db.models import Avg
from django.db.utils import IntegrityError
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, permissions, status, viewsets
from rest_framework.decorators import action, api_view
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken
from reviews.models import Category, Genre, Review, Title
from users.models import User

from api.serializers import (CategorySerializer, CommentSerializer,
                             GenreSerializer, RegisterDataSerializer,
                             ReviewSerializer, TitleSerializerGet,
                             TitleSerializerPost, TokenSerializer,
                             UserEditSerializer, UserSerializer)


@api_view(['POST'])
def register(request):
    serializer = RegisterDataSerializer(data=request.data)
    if User.objects.filter(
        username=request.data.get('username'),
        email=request.data.get('email')
    ).exists():
        return Response(request.data, status=status.HTTP_200_OK)
    serializer.is_valid(raise_exception=True)
    try:
        user, create = User.objects.get_or_create(
            **serializer.validated_data
        )
    except IntegrityError:
        raise ValidationError('Неверное имя пользователя или email')
    confirmation_code = default_token_generator.make_token(user)
    send_mail(
        subject='YaMDb регистрация',
        message=f'Ваш код подтверждения: {confirmation_code}',
        from_email=DEFAULT_FROM_EMAIL,
        recipient_list=[user.email],
    )

    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
def get_jwt_token(request):
    serializer = TokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = get_object_or_404(
        User,
        username=serializer.validated_data.get('username')
    )

    if default_token_generator.check_token(
        user, serializer.validated_data.get('confirmation_code')
    ):
        token = AccessToken.for_user(user)
        return Response({'token': str(token)}, status=status.HTTP_200_OK)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
    lookup_field = 'username'
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdmin,)
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    search_fields = ('username',)

    @action(
        methods=['GET', 'PATCH'],
        detail=False,
        permission_classes=[permissions.IsAuthenticated],
        serializer_class=UserEditSerializer,
    )
    def me(self, request):
        serializer = self.get_serializer(
            request.user,
            data=request.data,
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        if request.method == 'PATCH':
            serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (UserAdminModeratorOrReadOnly,)

    def get_title(self):
        return get_object_or_404(Title, id=self.kwargs.get('title_id'))

    def get_queryset(self):
        return self.get_title().review.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, title=self.get_title())


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (UserAdminModeratorOrReadOnly,)

    def get_review(self):
        return get_object_or_404(Review, id=self.kwargs.get('review_id'))

    def get_queryset(self):
        return self.get_review().comment.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, review=self.get_review())


class CategoryViewSet(GetPostDeleteViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class GenreViewSet(GetPostDeleteViewSet):
    queryset = Genre.objects.all().order_by('id')
    serializer_class = GenreSerializer


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.annotate(rating=Avg('review__score')
                                      ).order_by('id')
    serializer_class = TitleSerializerGet
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter)
    filterset_class = TitleFilter
    ordering_fields = ('name',)

    def get_serializer_class(self):
        if self.action == 'retrieve' or self.action == 'list':
            return TitleSerializerGet
        return TitleSerializerPost
