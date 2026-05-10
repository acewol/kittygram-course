from django.urls import include, path
from rest_framework.routers import DefaultRouter

from blog.views import BlogPostViewSet, CommentViewSet
from seasons.views import SeasonResultViewSet, SeasonViewSet
from .views import AchievementViewSet, CatViewSet


router = DefaultRouter()
router.register('cats', CatViewSet, basename='cats')
router.register('achievements', AchievementViewSet, basename='achievements')
router.register('blog/posts', BlogPostViewSet, basename='blog-posts')
router.register('blog/comments', CommentViewSet, basename='blog-comments')
router.register('seasons', SeasonViewSet, basename='seasons')
router.register(
    'season-results',
    SeasonResultViewSet,
    basename='season-results'
)

urlpatterns = [
    path('', include(router.urls)),
]