from django.urls import include
from django.urls import path

urlpatterns = [
    path("", include("apps.core.urls")),
    path(
        "dashboard/",
        include("apps.dashboard.urls", namespace="dashboard"),
    ),
    path(
        "profile/",
        include("apps.profiles.urls", namespace="profile"),
    ),
    path(
        "enterprise/",
        include("apps.enterprise.urls", namespace="enterprise"),
    ),
]
