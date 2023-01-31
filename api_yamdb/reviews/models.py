from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.validators import (
    MaxValueValidator,
    MinValueValidator,
    RegexValidator
)
from django.db import models
from django.utils import timezone
from rest_framework import serializers

from api_yamdb.settings import DEFAULT_EMAIL_LENGTH, DEFAULT_FIELD_LENGTH


class UsernameValidatorMixin:
    username = models.CharField(
        max_length=DEFAULT_FIELD_LENGTH,
        verbose_name='Имя пользователя',
        unique=True,
        null=True,
        validators=[RegexValidator(
            regex=r'^[\w.@+-]+$',
            message='Имя пользователя содержит недопустимый символ'
        )]
    )

    def validate_username(self, value):
        if value.lower() == "me":
            raise serializers.ValidationError(
                "Имя пользователя 'me'- не доступно"
            )
        return value


class User(AbstractUser, UsernameValidatorMixin):
    ADMIN = 'admin'
    MODERATOR = 'moderator'
    USER = 'user'
    ROLES = (
        (ADMIN, 'Administrator'),
        (MODERATOR, 'Moderator'),
        (USER, 'User'),
    )

    email = models.EmailField(
        verbose_name='Адрес электронной почты',
        unique=True,
        max_length=DEFAULT_EMAIL_LENGTH
    )
    role = models.CharField(
        verbose_name='Роль',
        max_length=DEFAULT_FIELD_LENGTH,
        choices=ROLES,
        default=USER
    )
    bio = models.TextField(
        verbose_name='О себе',
        null=True,
        blank=True
    )

    @property
    def is_moderator(self):
        return self.role == self.MODERATOR

    @property
    def is_admin(self):
        return self.role == self.ADMIN or self.is_superuser or self.is_staff

    @property
    def is_user(self):
        return self.role == self.USER

    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = ['username']

    class Meta:
        ordering = ('id', )
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username


class NameSlugModel(models.Model):
    name = models.CharField(
        max_length=settings.MAX_LENGTH_NAME,
        verbose_name='Название')
    slug = models.SlugField(
        unique=True,
        max_length=settings.SLUG_LENGTH,
        verbose_name='Слаг')

    class Meta:
        abstract = True
        ordering = ('name',)

    def __str__(self):
        return f'{self.name}'


class Category(NameSlugModel):
    class Meta(NameSlugModel.Meta):
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Genre(NameSlugModel):
    class Meta(NameSlugModel.Meta):
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'


def get_year():
    return timezone.now().year


class Title(models.Model):
    name = models.CharField(
        max_length=settings.MAX_LENGTH_NAME,
        verbose_name='Название')
    year = models.PositiveSmallIntegerField(
        default=1,
        validators=[MaxValueValidator(get_year)],
        verbose_name='Год'
    )
    category = models.ForeignKey(
        Category,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='categories',
        verbose_name='Категория',
    )
    genre = models.ManyToManyField(
        Genre,
        through='GenreTitle',
        related_name='genries',
        verbose_name='Жанр',
    )
    description = models.TextField(verbose_name='Описание')

    class Meta:
        ordering = ('name',)
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return f'{self.name}'


class GenreTitle(models.Model):
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    title = models.ForeignKey(Title, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.genre} {self.title}'


class ReviewAndComment(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE,
        verbose_name='Автор'
    )
    pub_date = models.DateTimeField(auto_now_add=True)
    text = models.TextField('Текст')

    class Meta:
        abstract = True
        ordering = ('-pub_date',)


class Review(ReviewAndComment):
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE,
        verbose_name='Произведение'
    )
    score = models.PositiveSmallIntegerField(
        validators=(MinValueValidator(1),
                    MaxValueValidator(10)),
        error_messages={'validators': 'Оценки могут быть от 1 до 10'},
        default=1
    )

    class Meta(ReviewAndComment.Meta):
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'author'],
                name='unique_author_review'
            )
        ]
        default_related_name = 'review'
        verbose_name = 'Ревью'
        verbose_name_plural = 'Ревью'

    def __str__(self):
        return self.text[0:15]


class Comment(ReviewAndComment):
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE,
        verbose_name='Отзыв'
    )

    class Meta(ReviewAndComment.Meta):
        default_related_name = 'comment'
        verbose_name = 'Коментарий'
        verbose_name_plural = 'Коментарии'

    def __str__(self):
        return self.text[0:30]
