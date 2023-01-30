from django.urls import include, path
from rest_framework import routers
from .views import (CategoryViewSet, GenreViewSet, TitleViewSet)


v1_router = routers.DefaultRouter()
v1_router.register('genres', GenreViewSet, basename='genres')
v1_router.register('categories', CategoryViewSet, basename='categories')
v1_router.register('titles', TitleViewSet, basename='titles')

urlpatterns = [
    path('v1/', include(v1_router.urls)),
]

# api/v1/categories/
# api/v1/categories/{slug}/

# api/v1/genres/
# api/v1/genres/{slug}/

# api/v1/titles/
# api/v1/titles/{titles_id}/


# api/v1/titles/{title_id}/reviews/
# api/v1/titles/{title_id}/reviews/{review_id}/

# api/v1/titles/{title_id}/reviews/{review_id}/comments/
# api/v1/titles/{title_id}/reviews/{review_id}/comments/{comment_id}/


# api/v1/auth/signup/
# api/v1/auth/token/

# api/v1/users/
# api/v1/users/{username}/
# api/v1/users/me/
