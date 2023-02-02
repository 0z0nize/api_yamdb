from core.routers import NoPutRouter
from django.urls import include, path

from .views import (CategoryViewSet, CommentViewSet, GenreViewSet,
                    ReviewViewSet, TitleViewSet, UserViewSet, get_jwt_token,
                    register)

router_v1 = NoPutRouter()

router_v1.register(r'users', UserViewSet, basename='users')
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews', ReviewViewSet,
    basename='reviews'
)
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet, basename='comments'
)
router_v1.register('categories', CategoryViewSet, basename='categories')
router_v1.register('genres', GenreViewSet, basename='genres')
router_v1.register('titles', TitleViewSet, basename='titles')

auth_urlpatterns = [
    path('signup/', register, name='register'),
    path('token/', get_jwt_token, name='token')
]

v1_urlpatterns = [
    path('', include(router_v1.urls)),
    path('auth/', include(auth_urlpatterns)),
]

urlpatterns = [
    path('v1/', include(v1_urlpatterns)),
]
