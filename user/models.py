from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.core.validators import RegexValidator
from django.db import models
from django.contrib.auth import get_user_model



class UserManager(BaseUserManager):
    """
    Manager to work with custom user model
    """

    def create_user(self, email, name, password=None):
        # Create a new user
        if not email:
            raise ValueError("Users must have a email address")
        email = self.normalize_email(email)
        user = self.model(email=email, name=name)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, name, password):
        # Create a new superuser.
        user = self.create_user(email, name, password)
        user.is_superuser = True
        user.is_staff = True
        user.save()
        return user


class UserProfile(AbstractBaseUser, PermissionsMixin):
    """
    Represents a user in the system
    """

    email = models.EmailField(max_length=255, unique=True, help_text="Email id of user")
    name = models.CharField(max_length=255, help_text="Name of the user")
    phone = models.CharField(
        max_length=10,
        null=True,
        blank=True,
        validators=[
            RegexValidator(
                regex="^[0-9]{10}$", message="Enter valid number (10 digits only)"
            )
        ],
        help_text="Phone Number",
    )
    about = models.TextField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_invited = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name"]

    def get_full_name(self):
        return self.name

    def get_short_name(self):
        return self.name

    def __str__(self):
        return str(self.name)

    def to_representation(self):
        rep = {
            "email": self.email,
            "name": self.name,
            "phone": self.phone,
            "about": self.about,
            "is_active": self.is_active,
            "is_staff": self.is_staff,
            "is_invited": self.is_invited,
            "is_verified": self.is_verified,
            "date_joined": self.date_joined,
            "groups": [
                {"id": group.id, "name": group.name} for group in self.groups.all()
            ],
            "profile_links": [
                profile_link.to_representation()
                for profile_link in self.profile_links_user.all()
            ],
        }

        return rep

UserModel = get_user_model()

class UserFollowing(models.Model):

    user_id = models.ForeignKey(UserProfile, related_name="following", on_delete=models.CASCADE)
    following_user_id = models.ForeignKey(UserProfile, related_name="followers", on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user_id','following_user_id'],  name="unique_followers")
        ]

    def __str__(self):
        return f"{self.user_id} follows {self.following_user_id}"