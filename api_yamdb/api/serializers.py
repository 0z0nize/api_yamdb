from rest_framework import serializers
from reviews.models import Category, Genre, Title


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fiels = '__all__'


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        fiels = '__all__'


class TitleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Title
        fiels = '__all__'
