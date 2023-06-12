from django.contrib.auth import get_user_model
from django.contrib.auth.models import update_last_login
from rest_framework import exceptions, serializers, status
from rest_framework_simplejwt.settings import api_settings
from media.models import Post, Comment, Like

from user.utils import APIException, get_tokens_for_user

User = get_user_model()



class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = (
            "id",
            "user",
            "title",
            "description",
            "created",
        )
    def to_representation(self, instance):
        rep = super().to_representation(instance)
        print(instance)
        rep["likes"] = len(Like.objects.filter(post=instance.id))
        rep["comments"]=[comment.to_representation() for comment in Comment.objects.filter(post =instance.id)]
        return rep


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = (
            "id",
            "post",
            "text",
        )

class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = (
            "id",
            "post",
            "user",
        )
