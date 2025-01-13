from typing import Any

from allauth.account.views import PasswordResetView as AllauthPasswordResetView
from django.contrib.auth.decorators import login_not_required
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View

from front.users.forms import PasswordResetForm
from front.users.models import User


def _find_user_by_email(request):
    email = request.GET.get("email")
    return User.objects.filter(email=email)


@login_not_required
def check_email_address_view(request, *args, **kwargs):
    user_exists = _find_user_by_email(request)
    return JsonResponse(
        {
            "exists": user_exists.exists(),
            "detail": "Email is already in use" if user_exists.exists() else "",
        },
    )


@login_not_required
def check_email_address_for_password_reset(request, *args, **kwargs):
    user_exists = _find_user_by_email(request)
    if user_exists.exists():
        return JsonResponse({"exists": True, "detail": ""}, status=200)
    return JsonResponse(
        {"exists": False, "detail": "No such user with the provided email!"},
        status=400,
    )

@method_decorator(login_not_required, name="dispatch")
class _PasswordResetView(View):
    form_class = PasswordResetForm

    def post(self, request, *args, **kwargs):
        return JsonResponse({"detail": "Check your email for reset link"}, status=200)


password_reset_view = _PasswordResetView.as_view()


def password_reset_done_view(request, *args, **kwargs):
    return JsonResponse({}, status=200)


def password_reset_confirm_view(request, *args, **kwargs):
    return JsonResponse({}, status=200)


def password_reset_complete_view(request, *args, **kwargs):
    return JsonResponse({}, status=200)


def password_update_view(request, *args, **kwargs):
    return JsonResponse({}, status=200)


def check_username_view(request, *args, **kwargs):
    return JsonResponse({}, status=200)


def check_password_strength_view(request, *args, **kwargs):
    return JsonResponse({}, status=200)


def check_password_confirmation_view(request, *args, **kwargs):
    return JsonResponse({}, status=200)


def check_phone_number_view(request, *args, **kwargs):
    return JsonResponse({}, status=200)
