from allauth.account.forms import SignupForm
from allauth.socialaccount.forms import SignupForm as SocialSignupForm
from django.contrib.auth import forms as admin_forms
from django.forms import EmailField, Form, CharField, widgets, BooleanField
from django.utils.translation import gettext_lazy as _
from allauth.account.forms import ResetPasswordForm

from .models import User


class UserAdminChangeForm(admin_forms.UserChangeForm):
    class Meta(admin_forms.UserChangeForm.Meta):  # type: ignore[name-defined]
        model = User
        field_classes = {"email": EmailField}


class UserAdminCreationForm(admin_forms.UserCreationForm):
    """
    Form for User Creation in the Admin Area.
    To change user signup, see UserSignupForm and UserSocialSignupForm.
    """

    class Meta(admin_forms.UserCreationForm.Meta):  # type: ignore[name-defined]
        model = User
        fields = ("email",)
        field_classes = {"email": EmailField}
        error_messages = {
            "email": {"unique": _("This email has already been taken.")},
        }



class UserSignupForm(SignupForm):
    """
    Form that will be rendered on a user sign up section/screen.
    Default fields will be added automatically.
    Check UserSocialSignupForm for accounts created from social.
    """

    password_show = BooleanField(
        required=False,
        widget=widgets.CheckboxInput(),
    )
    accept_terms = BooleanField(
        required=False,
        label="""
        I have read and accept the
        <a class="text-dark-emphasis" role='button'>Privacy Policy</a>""",
        help_text="You must accept the terms and conditions.",
        widget=widgets.CheckboxInput(attrs={"class": "form-check-input"}),
    )


class UserSocialSignupForm(SocialSignupForm):
    """
    Renders the form when user has signed up using social accounts.
    Default fields will be added automatically.
    See UserSignupForm otherwise.
    """


class AuthenticationForm(Form):
    email = CharField(
        label=_("Email Address"),
        max_length=254,
        widget=widgets.EmailInput(
            attrs={
                "class": "form-control form-control-lg",
                "placeholder": "Email Address",
            },
        ),
    )
    password = CharField(
        label=_("Password"),
        strip=False,
        widget=widgets.PasswordInput(
            attrs={
                "class": "form-control form-control-lg",
                "autocomplete": "",
                "placeholder": "Password",
            },
        ),
    )
    memory = BooleanField(
        label="Remember for 30 days",
        initial=False,
        required=False,
        widget=widgets.CheckboxInput(attrs={"class": "form-check-input"}),
    )


class PasswordResetForm(ResetPasswordForm):
    """ ""
    Form for user password reset.
    """

    email = EmailField(
        label=_("Email Address"),
        max_length=254,
        widget=widgets.EmailInput(
            attrs={
                "class": "form-control form-control-lg",
                "id": "signupModalFormResetPasswordEmail",
                "placeholder": "Enter your email address",
                "aria-label": "Enter your email address",
            },
        ),
    )
