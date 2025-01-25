import base64
import hashlib

from django import forms
from django.core.exceptions import ValidationError

from .models import Organization


class OrganizationForm(forms.ModelForm):
    """Form definition for Organization."""

    visibility = forms.ChoiceField(
        label="Organization Visibility",
        choices=(("PRIVATE", "Private"), ("PUBLIC", "Public")),
        initial="PUBLIC",
        widget=forms.Select(
            attrs={
                "class": "js-select form-select",
                "title": "visibility",
            },
        ),
    )
    name = forms.CharField(
        label="Organization Name",
        initial="",
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Organization Name",
            },
        ),
    )

    class Meta:
        """Meta definition for Organization."""

        model = Organization
        fields = ("name", "visibility")

    def __init__(self, *args, **kwargs):
        # Profile passed to the form
        self.profile = kwargs.pop("profile", None)
        super().__init__(*args, **kwargs)

    def clean(self):
        """Validate the organization limits based on the user's plan."""
        cleaned_data = super().clean()

        if not self.profile:
            msg = "Profile information is required to validate limits."
            raise ValidationError(msg)

        # Define organization limits based on plan
        plan_limits = {
            "F": 1,
            "S": 2,
            "P": 4,
        }  # Example: Free (F), Standard (S), Premium (P)
        limit = plan_limits.get(self.profile.plan, float("inf"))

        if self.profile.organizations_count >= int(limit + 1):
            message = """
            You've exhausted the number of organizations for this profile.
            Please consider upgrading your plan.
            """
            raise ValidationError(
                {
                    "name": ValidationError(
                        message=message.strip(),
                        code="organization_limit_exceeded",
                    ),
                },
            )
        return cleaned_data

    def save(self, commit=True):  # noqa: FBT002
        """Save the form and update the profile's organizations count."""
        # Call the parent save method to save the form instance
        instance = super().save(commit=False)

        if not self.profile:
            msg = "Profile information is required to save the organization."
            raise ValueError(msg)
        # Save the instance to the database
        profile_id = str(self.profile.id)
        name_and_profile_id = profile_id + self.cleaned_data.get("name")
        hashed_object = hashlib.sha256(name_and_profile_id.encode()).digest()
        hashed_bytes = base64.urlsafe_b64encode(hashed_object)
        instance.profile = self.profile
        if commit:
            instance.hashed_name = hashed_bytes.decode("utf-8").rstrip("=")[:100]
            instance.save()
            self.profile.organizations_count += 1
            self.profile.save()
        return instance

