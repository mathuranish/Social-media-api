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
from media.models import Post,Comment,Like
from media.serializers import (
    PostSerializer,
    CommentSerializer,
    LikeSerializer
)

user = get_user_model()

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

    def perform_create(self, serializer):
        if self.request.user.is_authenticated:
            serializer.save(user=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
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

class PostViewSet(BaseViewset):
    permission_classes = (IsAuthenticated,)
    serializer_class = PostSerializer
    queryset = Post.objects.all()

class CommentViewSet(BaseViewset):
    permission_classes = (IsAuthenticated,)
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()

class LikeViewSet(BaseViewset):
    permission_classes = (IsAuthenticated,)
    serializer_class = LikeSerializer
    queryset = Like.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        data = request.data
        serializer.is_valid(raise_exception=True)
        if Like.objects.filter(user = self.request.user, post= int(data["post"])).exists():
            print(data)
            obj = Like.objects.get(user = self.request.user, post= int(data["post"]))
            obj.delete()
            headers = self.get_success_headers(serializer.data)
            return get_response(
                data="Like removed",
                status_code=status.HTTP_201_CREATED,
                headers=headers,
            )
        else:
            # serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return get_response(
                data=serializer.data,
                status_code=status.HTTP_201_CREATED,
                headers=headers,
            )