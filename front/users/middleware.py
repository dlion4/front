from django.contrib.auth.middleware import (  # type: ignore  # noqa: PGH003
    LoginRequiredMiddleware as RequireLoginMiddleware,
)


class LoginRequiredMiddleware(RequireLoginMiddleware):
    """
    Middleware to ensure login is required for all views except those under /accounts/.
    """
    def process_view(self, request, view_func, view_args, view_kwargs):
        if request.path.startswith("/accounts/"):
            return None
        return super().process_view(request, view_func, view_args, view_kwargs)
