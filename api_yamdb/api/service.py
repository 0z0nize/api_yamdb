from django_filters import rest_framework
from rest_framework import filters, mixins, viewsets

from .permissions import IsAdminOrReadOnly
from reviews.models import Title
from .permissions import IsAdminOrReadOnly


class TitleFilter(rest_framework.FilterSet):
    category = rest_framework.CharFilter(field_name='category__slug')
    genre = rest_framework.CharFilter(field_name='genre__slug')
    name = rest_framework.CharFilter(field_name='name', lookup_expr='contains')
    year = rest_framework.NumberFilter()

    class Meta:
        model = Title
        fields = ('category', 'genre', 'name', 'year',)


class GetPostDeleteViewSet(mixins.CreateModelMixin,
                           mixins.DestroyModelMixin,
                           mixins.ListModelMixin,
                           viewsets.GenericViewSet):
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'
