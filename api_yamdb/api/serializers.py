from api_yamdb.settings import DEFAULT_EMAIL_LENGTH, DEFAULT_FIELD_LENGTH
from core.validators import (SCORE_VALIDATOR, UsernameValidatorMixin,
                             validate_release_year)
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from rest_framework.validators import UniqueValidator
from reviews.models import Category, Comment, Genre, Review, Title
from users.models import User


class UserSerializer(serializers.ModelSerializer, UsernameValidatorMixin):
    email = serializers.EmailField(
        max_length=DEFAULT_EMAIL_LENGTH,
        validators=[UniqueValidator(queryset=User.objects.all())],
        required=True,
    )

    class Meta:
        fields = ('username', 'email', 'first_name',
                  'last_name', 'bio', 'role')
        model = User


class UserEditSerializer(UserSerializer):
    class Meta(UserSerializer.Meta):
        read_only_fields = ('role',)


class RegisterDataSerializer(
    serializers.HyperlinkedModelSerializer, UsernameValidatorMixin
):
    email = serializers.EmailField(
        max_length=DEFAULT_EMAIL_LENGTH,
        required=True,
    )

    class Meta:
        fields = ('username', 'email')
        model = User


class TokenSerializer(serializers.Serializer, UsernameValidatorMixin):
    username = serializers.CharField(required=True,)
    confirmation_code = serializers.CharField(
        max_length=DEFAULT_FIELD_LENGTH, required=True,
    )


class ReviewSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(slug_field='username', read_only=True)
    title = SlugRelatedField(slug_field='name', read_only=True)
    score = serializers.IntegerField(
        validators=SCORE_VALIDATOR)

    class Meta:
        fields = '__all__'
        model = Review

    def validate(self, data):
        request = self.context['request']
        if (request.method not in ('GET', 'PATCH')
           and Review.objects.filter(
            title=get_object_or_404(
                Title, pk=self.context.get('view').kwargs.get('title_id')
            ),
                author=request.user).exists()):
            raise ValidationError('Вы уже писали ревью')
        return data


class CommentSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        fields = '__all__'
        model = Comment
        read_only_fields = ('review',)


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        exclude = ('id',)


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        exclude = ('id',)


class TitleSerializerGet(serializers.ModelSerializer):
    category = CategorySerializer()
    genre = GenreSerializer(many=True)
    rating = serializers.IntegerField(default=0)

    class Meta:
        model = Title
        fields = '__all__'
        read_only_fields = ('__all__',)


class TitleSerializerPost(serializers.ModelSerializer):
    category = SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all()
    )
    genre = SlugRelatedField(
        slug_field='slug',
        queryset=Genre.objects.all(),
        many=True
    )
    year = serializers.IntegerField()

    def to_representation(self, value):
        return TitleSerializerGet(self.instance).data

    def validate_year(self, value):
        return validate_release_year(value)

    class Meta:
        model = Title
        fields = '__all__'
