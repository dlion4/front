from typing import Any

from allauth.account.views import LogoutView as AllauthLogoutView
from django.conf import settings
from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_not_required
from django.contrib.auth.models import User
from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from django.utils.timezone import now
from django.views import View
from django.views.generic.edit import FormView


from .forms import AuthenticationForm
from .forms import PasswordResetForm
from .forms import UserSignupForm


class LoginView(FormView):
    template_name = "account/login.html"
    form_class = AuthenticationForm
    @method_decorator(login_not_required)
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(settings.LOGIN_REDIRECT_URL)
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["reset_password"] = PasswordResetForm()
        return context

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            return self.form_valid(form)
        return JsonResponse({"detail": form.errors.get_json_data()}, status=400)

    def form_valid(self, form: AuthenticationForm) -> JsonResponse:
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        user = authenticate(self.request, username=email, password=password)
        if user is not None:
            login(self.request, user)
            return JsonResponse(
                {
                    "detail": "Logged in successfully.",
                    "user_id": str(user.id),
                    "url": str(settings.LOGIN_REDIRECT_URL),
                },
                status=200,
            )
        return JsonResponse(
            {"detail": "No user with the provided credentials"}, status=404)


class LogoutView(AllauthLogoutView):
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class UserRegistrationView(FormView):
    form_class = UserSignupForm
    @method_decorator(login_not_required)
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(settings.LOGIN_REDIRECT_URL)
        return super().dispatch(request, *args, **kwargs)
    @method_decorator(transaction.atomic)
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = form.save(request=request)
            user.username = user.handle_username
            user.save()
            return JsonResponse(
                {
                    "detail": "User created successfully.",
                    "user_id": str(user.id),
                    "url": str(settings.LOGIN_URL),
                },
                status=201,
            )
        return JsonResponse({"detail": form.errors.get_json_data()}, status=400)
