from __future__ import annotations

import contextlib
import typing
from contextlib import contextmanager

from allauth.account.adapter import DefaultAccountAdapter
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.conf import settings
from django.db import IntegrityError

from front.users.models import Profile

if typing.TYPE_CHECKING:
    from allauth.socialaccount.models import SocialLogin
    from django.http import HttpRequest

    from front.users.models import User


class AccountAdapter(DefaultAccountAdapter):
    def is_open_for_signup(self, request: HttpRequest) -> bool:
        return getattr(settings, "ACCOUNT_ALLOW_REGISTRATION", True)


class SocialAccountAdapter(DefaultSocialAccountAdapter):
    def is_open_for_signup(
        self,
        request: HttpRequest,
        sociallogin: SocialLogin,
    ) -> bool:
        return getattr(settings, "ACCOUNT_ALLOW_REGISTRATION", True)

    def populate_user(
        self,
        request: HttpRequest,
        sociallogin: SocialLogin,
        data: dict[str, typing.Any],
    ) -> User:
        """
        Populates user information from social provider info.
        See: https://docs.allauth.org/en/latest/socialaccount/advanced.html#creating-and-populating-user-instances
        """
        user: User = super().populate_user(request, sociallogin, data)
        extra_data: dict = sociallogin.account.extra_data
        user.username = (
            user.username or extra_data.get("name") or extra_data.get("login")
        )
        user.social_uid = (
            user.social_uid or extra_data.get("id") or extra_data.get("sub")
        )
        _handle_profile_creation_update(user, extra_data)
        return user


@contextmanager
def create_profile_form_user(user: User, data: dict):
    """
    Context manager to update a user's profile fields safely.
    """
    with contextlib.suppress(Exception):
        profile = user.user_profile
        profile.first_name = profile.first_name or data.get("first_name", "").strip()
        if last_name := data.get("last_name", "").strip():
            profile.last_name = f"{profile.last_name or ''} {last_name}".strip()
    yield


def _handle_profile_creation_update(user, user_data):
    print("Handling profile creation/update...")
    print("user social_uid: ", user.social_uid)
    print("user_data:", user_data)
    # 113825375903421253407 -GOOGLE - Uid
    # 96693702 -GITHUB - Uid
