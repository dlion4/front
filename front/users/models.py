import uuid
from typing import ClassVar

from django.contrib.auth.models import AbstractUser
from django.db.models import CASCADE
from django.db.models import CharField
from django.db.models import EmailField, BigIntegerField
from django.db.models import Model
from django.db.models import OneToOneField, URLField
from django.db.models import UUIDField
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.db import transaction
from .managers import UserManager


class User(AbstractUser):
    """
    Default custom user model for metronic developer.
    If adding fields that need to be filled at user signup,
    check forms.SignupForm and forms.SocialSignupForms accordingly.
    """

    id = UUIDField(
        primary_key=True,
        unique=True,
        editable=False,
        default=uuid.uuid4,  # Use callable, not function call
        db_comment="Unique UUID for the user instead of a numeric ID",
    )
    social_uid = BigIntegerField(_("Social UUID"),blank=True, null=True)
    email = EmailField(
        _("email address"),
        unique=True,
        help_text=_("The user's email address, used for authentication."),
    )
    username = CharField(  # noqa: DJ001
        _("username"),
        blank=True,
        null=True,
        help_text=_("Optional username for the user."),
    )
    site_email = EmailField(max_length=255, blank=True, null=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects: ClassVar[UserManager] = UserManager()

    def get_absolute_url(self) -> str:
        return reverse("users:detail", kwargs={"pk": self.id})

    @property
    def handle_username(self):
        return self.username or self.email.split("@")[0]
    @property
    def handle_site_email(self):
        return f"{self.handle_username}@front.com"
    def save(self, *args, **kwargs):
        if not self.site_email:
            self.site_email = self.handle_site_email
        super().save(*args, **kwargs)


class Profile(Model):
    """Model definition for Profile."""

    id = UUIDField(
        primary_key=True,
        unique=True,
        editable=False,
        default=uuid.uuid4,  # Use callable, not function call
        db_comment="Unique UUID for the profile instead of a numeric ID",
    )
    user = OneToOneField(User, on_delete=CASCADE, related_name="user_profile")
    first_name = CharField(  # noqa: DJ001
        _("First Name"), max_length=100, blank=True, null=True,
    )
    last_name = CharField(  # noqa: DJ001
        _("Last Name"), max_length=100, blank=True, null=True  # noqa: COM812
    )
    avatar_url = URLField(  # noqa: DJ001
        _("Social Avatar"), max_length=255, blank=True, null=True,
    )

    class Meta:
        """Meta definition for Profile."""

        verbose_name = "Profile"
        verbose_name_plural = "Profiles"
        db_table = "users_profiles"

    def __str__(self):
        """Unicode representation of Profile."""
        return f"{self.user.username}"



    def get_absolute_url(self):
        """Return absolute url for Profile."""
        return ""

    # TODO: Define custom methods here
