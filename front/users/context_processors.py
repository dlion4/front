from django.conf import settings

from .forms import AuthenticationForm
from .forms import PasswordResetForm
from .forms import UserAdminCreationForm


def allauth_settings(request):
    """Expose some settings from django-allauth in templates."""
    return {
        "ACCOUNT_ALLOW_REGISTRATION": settings.ACCOUNT_ALLOW_REGISTRATION,
        "login_form": AuthenticationForm(),
        "signup_form": UserAdminCreationForm(),
        "password_rest_form": PasswordResetForm(),
    }
