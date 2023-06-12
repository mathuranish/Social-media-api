from django.urls import path
from media.views import PostViewSet, CommentViewSet, LikeViewSet

from rest_framework import routers
router = routers.DefaultRouter()

# urlpatterns = [
#     path('', views.index, name='index'),
#     path('upload', views.upload, name='upload'),
#     path('follow', views.follow, name='follow'),
#     path('search', views.search, name='search'),
#     path('profile/<str:pk>', views.profile, name='profile'),
#     path('like-post', views.like_post, name='like-post'),
# ]

router.register("post", PostViewSet, basename="post")
router.register("like", LikeViewSet, basename="post")
router.register("unlike", LikeViewSet, basename="post")
router.register("comment", CommentViewSet, basename="post")


urlpatterns = router.urls

