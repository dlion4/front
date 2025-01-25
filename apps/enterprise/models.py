import base64
import hashlib
import uuid

from django.db import models
from django.forms import ValidationError
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from front.users.models import Profile

# Create your models here.


class Organization(models.Model):
    """Model definition for Organization."""

    id = models.UUIDField(
        primary_key=True,
        unique=True,
        editable=False,
        default=uuid.uuid4,
        db_comment="Unique UUID for the organization",
    )
    profile = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        related_name="profile_organizations",
    )
    name = models.CharField(_("Organization Name"), max_length=200)
    hashed_name = models.CharField(max_length=100, blank=True, editable=False)
    project_count = models.IntegerField(
        _("Project Count"),
        help_text="The maximum number of projects per Organization",
        default=0,
    )
    visibility = models.CharField(
        choices=(("PRIVATE", "Private"), ("PUBLIC", "Public")),
        max_length=20,
        default="PUBLIC",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    is_archived = models.BooleanField(default=False)
    is_archived_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Organization"
        verbose_name_plural = "Organizations"

    def __str__(self):
        return f"{self.name}"

    def save(self, *args, **kwargs):
        """Save method for Organization."""
        super().save(*args, **kwargs)
    def get_absolute_url(self):
        return self._absolute_url()


    def _absolute_url(self, kwargs_urls: dict | None = None) -> str:
        """
        Generate the absolute URL for the organization based on its hashed name.

        Args:
            kwargs_urls (dict | None): Additional keyword arguments for the URL.

        Returns:
            str: The absolute URL for the organization.
        """
        # Ensure kwargs_urls is initialized to an empty dictionary if None
        kwargs_urls = kwargs_urls or {}

        # Merge the default 'uuid' with any provided kwargs
        kwargs_urls = {"uuid": self.hashed_name} | kwargs_urls

        # Return the reversed URL
        # return reverse("dashboard:home", kwargs=kwargs_urls)
        return ""




class Project(models.Model):
    """Model definition for Project."""

    id = models.UUIDField(
        primary_key=True,
        unique=True,
        editable=False,
        default=uuid.uuid4,
        db_comment="Unique UUID for the Project",
    )
    profile = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        related_name="profile_projects",
    )
    organization = models.ForeignKey(
        Organization,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="organization_projects",
    )
    name = models.CharField(_("Project Name"), max_length=200)

    class Meta:
        """Meta definition for Project."""

        verbose_name = "Project"
        verbose_name_plural = "Projects"

    def __str__(self):
        """Unicode representation of Project."""
        return self.name

    def save(self, *args, **kwargs):
        """Save method for Project."""
        self.clean()
        self.organization.project_count += 1
        self.organization.save()
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        """Return absolute url for Project."""
        return ""

    def clean(self):
        """Validate the project limits based on the user's plan."""
        plan_project_limits = {"F": 2, "S": 4, "P": 10}
        project_limit = plan_project_limits.get(self.profile.plan, float("inf"))

        if self.organization.project_count >= project_limit:
            raise ValidationError(
                {
                    "organization": ValidationError(
                        message=_(
                            "You've reached the maximum number of projects for this organization "  # noqa: E501
                            "under your current plan. Please upgrade your plan to add more projects.",  # noqa: E501
                        ),
                        code="project_limit_exceeded",
                    ),
                },
            )
