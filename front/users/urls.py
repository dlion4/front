import time

from django.urls import include
from django.urls import path

from ._authorize import LoginView
from ._authorize import LogoutView
from ._authorize import PasswordResetRequestView
from ._authorize import UserRegistrationView
from .actions import views
from .views import user_detail_view
from .views import user_redirect_view
from .views import user_update_view

app_name = "users"
urlpatterns = [
    path("~redirect/", view=user_redirect_view, name="redirect"),
    path("~update/", view=user_update_view, name="update"),
    path("<int:pk>/", view=user_detail_view, name="detail"),
    path("authenticate/", view=LoginView.as_view(), name="login"),
    path("logout/", view=LogoutView.as_view(), name="logout"),
    path(
        "login-callback/",
        view=views.social_login_callback_view,
        name="login_callback_view",
    ),
    path(
        "developer-registration/",
        UserRegistrationView.as_view(template_name="account/register.html"),
        {
            "template_name": "users/register.html",
            "time": str(time.time()),
        },
        name="register",
    ),
    path(
        # NOTE: This is not best practice
        "password/",
        include(
            [
                path(
                    "reset",
                    include(
                        [
                            path(
                                "reset/",
                                PasswordResetRequestView.as_view(),
                                name="password_reset_request_view",
                            ),
                            path(
                                "reset/<uidb64>/<token>/",
                                include(
                                    [
                                        path(
                                            "",
                                            views.password_reset_confirm_view,
                                            name="password_reset_confirm_view",
                                        ),
                                    ],
                                ),
                            ),
                        ],
                    ),
                ),
            ],
        ),
    ),
    # Add this line to your urlpatterns
    path(
        "actions/",
        include(
            [
                path(
                    "check_email/",
                    include(
                        [
                            path(
                                "",
                                views.check_email_address_view,
                                name="check_email_view",
                            ),
                            path(
                                "reset/",
                                views.check_email_address_for_password_reset,
                                name="check_email",
                            ),
                        ],
                    ),
                ),
                path(
                    "password/",
                    include(
                        [
                            path(
                                "reset/",
                                views.password_reset_view,
                                name="password_reset_request_view",
                            ),
                            path(
                                "reset/done/",
                                views.password_reset_done_view,
                                name="password_reset_done_view",
                            ),
                            path(
                                "reset/<uidb64>/<token>/",
                                views.password_reset_confirm_view,
                                name="password_reset_confirm_view",
                            ),
                            path(
                                "reset/complete/",
                                views.password_reset_complete_view,
                                name="password_reset_complete_view",
                            ),
                            path(
                                "update/<uidb64>/<token>/",
                                views.password_update_view,
                                name="password_update_view",
                            ),
                        ],
                    ),
                ),
            ],
        ),
    ),
]
