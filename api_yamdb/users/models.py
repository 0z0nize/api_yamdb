from core.validators import UsernameValidatorMixin
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models


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
        max_length=settings.DEFAULT_EMAIL_LENGTH
    )
    role = models.CharField(
        verbose_name='Роль',
        max_length=settings.DEFAULT_FIELD_LENGTH,
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
