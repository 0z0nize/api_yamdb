from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import (
    MaxValueValidator,
    MinValueValidator,
    RegexValidator,
)
from django.db import models
from django.utils import timezone
from rest_framework import serializers

SCORE_VALIDATOR = (
    MinValueValidator(settings.SCORE_MIN),
    MaxValueValidator(settings.SCORE_MAX),
)


class UsernameValidatorMixin:
    username = models.CharField(
        max_length=settings.DEFAULT_FIELD_LENGTH,
        verbose_name='Имя пользователя',
        unique=True,
        null=True,
        validators=[
            RegexValidator(
                regex=r'^[\w.@+-]+$',
                message='Имя пользователя содержит недопустимый символ',
            )
        ],
    )

    def validate_username(self, value):
        if value.lower() == 'me':
            raise serializers.ValidationError(
                "Имя пользователя 'me'- не доступно"
            )
        return value


def validate_release_year(title_year):
    if title_year > (timezone.now().year):
        raise ValidationError('Произведения из будущего нельзя добавлять')
    elif title_year < settings.PREHISTORIC_ART:
        raise ValidationError(
            'Изображение дикой свиньи на стене пещеры в Сулавеси, '
            'Индонезия является самым древним датированным произведением '
            'искусства возрастом 45500 лет до нашей эры. '
            'Сообщите пожалуйста разработчикам если произошло новое открытие.'
        )
    return title_year
