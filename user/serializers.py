from django.contrib.auth import get_user_model
from django.contrib.auth.models import update_last_login
from rest_framework import exceptions, serializers, status
from rest_framework_simplejwt.settings import api_settings
from user.models import UserFollowing

from user.utils import APIException, get_tokens_for_user

User = get_user_model()


class TokenObtainPairSerializer(serializers.Serializer):
    email = serializers.EmailField(required=False)
    password = serializers.CharField()

    def validate(self, data):
        email = data.get("email")
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise APIException(
                "User Does not exists", status_code=status.HTTP_404_NOT_FOUND
            )

        valid = user.check_password(data["password"])
        if valid:
            data = get_tokens_for_user(user)
            if api_settings.UPDATE_LAST_LOGIN:
                update_last_login(None, user)
        else:
            raise exceptions.AuthenticationFailed(
                "No active vendor found with the given credentials",
            )
        return data


class RegisterSerializer(serializers.Serializer):
    name = serializers.CharField()
    about = serializers.CharField()
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = (
            "id",
            "name",
            "about",
            "email",
            "password",
        )

    def validate(self, attrs):
        # checking is email exists
        email_exists = User.objects.filter(
            email=attrs["email"]
        ).exists()  # returns bool
        if email_exists:
            raise APIException("Email already exists")
        return super().validate(attrs)

    # we need to hash the user's passwords manually with this methord
    def create(self, validated_data):
        user = User.objects.create(
            email=validated_data["email"],
            password=validated_data["password"],
            name=validated_data["name"],
            about=validated_data["about"],
        )
        user.set_password(validated_data["password"])
        user.save()
        return user


class UserSerializer(serializers.ModelSerializer):
    following = serializers.SerializerMethodField()
    followers = serializers.SerializerMethodField()
    class Meta:
        model = User
        fields = (
            "id",
            "name",
            "about",
            "email",
            "following",
            "followers",
            "is_active",
            "is_staff",
            "is_superuser",
            "date_joined",
        )
        read_only_fields = (
            "id",
            "email",
            "is_active",
            "is_staff",
            "is_superuser",
            "date_joined",
        )
    def get_following(self, obj):
        return FollowingSerializer(obj.following.all(), many=True).data

    def get_followers(self, obj):
        return FollowersSerializer(obj.followers.all(), many=True).data

class UserFollowingSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserFollowing
        fields = (
            "id",
            "user_id",
            "following_user_id",
            "created",
        )

class FollowingSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserFollowing
        fields = ("id", "following_user_id", "created")

class FollowersSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserFollowing
        fields = ("id", "user_id", "created")
