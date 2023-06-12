from django.contrib.auth import get_user_model
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.views import TokenObtainPairView
from user.utils import ListPagination, get_response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.filters import OrderingFilter, SearchFilter

# from apps.user.permissions import UserPermission
from user.models import UserFollowing
from user.serializers import (
    RegisterSerializer,
    TokenObtainPairSerializer,
    UserSerializer,
    UserFollowingSerializer,
)


User = get_user_model()

class BaseViewset(ModelViewSet):
    authentication_classes = (JWTAuthentication,)
    pagination_class = ListPagination
    filter_backends = (OrderingFilter, SearchFilter)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return get_response(
            data=serializer.data,
            status_code=status.HTTP_200_OK,
        )

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return get_response(
            data=serializer.data,
            status_code=status.HTTP_200_OK,
        )

   

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        headers = self.get_success_headers(serializer.data)
        return get_response(
            data=serializer.data,
            status_code=status.HTTP_201_CREATED,
            headers=headers,
        )

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, "_prefetched_objects_cache", None):
            instance._prefetched_objects_cache = {}

        return get_response(serializer.data, status_code=status.HTTP_200_OK)




class TokenObtainPairView(TokenObtainPairView):
    serializer_class = TokenObtainPairSerializer


class RegisterView(CreateAPIView):
    serializer_class = RegisterSerializer
    model = get_user_model()



class UserViewset(BaseViewset):
    serializer_class = UserSerializer
    permission_classes = (
        IsAuthenticated,
    )
    queryset = User.objects.all().order_by("-id")
    swagger_tags = ["User"]
    http_method_names = ["get", "put", "patch"]
    filter_fields = [
        "id",
        "name",
        "about",
        "email",
        "is_active",
        "is_staff",
        "is_superuser",
        "date_joined",
    ]
    ordering_fields = [
        "id",
        "name",
        "about",
        "email",
        "is_active",
        "is_staff",
        "is_superuser",
        "date_joined",
    ]
    search_fields = [
        "name",
        "about",
        "email",
    ]

class UserFollowingViewSet(BaseViewset):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserFollowingSerializer
    queryset = UserFollowing.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        data = request.data
        serializer.is_valid(raise_exception=True)
        if UserFollowing.objects.filter(user_id = int(data["user_id"]), following_user_id= int(data["following_user_id"])).exists():
            print(data)
            obj = UserFollowing.objects.get(user_id = int(data["user_id"]), following_user_id= int(data["following_user_id"]))
            obj.delete()
            headers = self.get_success_headers(serializer.data)
            return get_response(
                data="Unfollowed",
                status_code=status.HTTP_201_CREATED,
                headers=headers,
            )
        else:
            # serializer.is_valid(raise_exception=True)
            serializer.save()
            headers = self.get_success_headers(serializer.data)
            return get_response(
                data=serializer.data,
                status_code=status.HTTP_201_CREATED,
                headers=headers,
            )