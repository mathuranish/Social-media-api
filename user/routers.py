from django.urls import path
from rest_framework import routers
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView

from user.views import RegisterView, TokenObtainPairView, UserViewset,UserFollowingViewSet

router = routers.DefaultRouter()

app_name = "user"

urlpatterns = [
    path("login/", TokenObtainPairView.as_view(), name="login"),
    path("register/", RegisterView.as_view(), name="register"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("token/verify/", TokenVerifyView.as_view(), name="token_verify"),
]

router.register("user", UserViewset, basename="user")
router.register("follow", UserFollowingViewSet, basename="follow")
router.register("unfollow", UserFollowingViewSet, basename="unfollow")


urlpatterns += router.urls
