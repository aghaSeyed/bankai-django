from django.urls import path, include
# from .views import PostAPIView, PostAPIDetail
from rest_framework.urlpatterns import format_suffix_patterns

from .views import CategoryViewSet
from rest_framework.routers import DefaultRouter


class NestedDefaultRouter(DefaultRouter):
    pass


router = NestedDefaultRouter()

router.register('category', CategoryViewSet, basename='category')

# posts_router = router.register('posts', PostViewSet)
#
# posts_router.register(
#     'comments',
#     CommentViewSet,
#     basename='comments',
#     parents_query_lookups=['post']
# )
#
# posts_router.register(
#     'likes',
#     LikeViewSet,
#     basename='likes',
#     parents_query_lookups=['post']
# )

urlpatterns = [
    path('', include(router.urls))
]
