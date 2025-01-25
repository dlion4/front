from django.urls import include
from django.urls import path

from .views import HomeView

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("partials/", include("apps.partials.urls", namespace="partials")),
]
