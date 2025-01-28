from django.urls import include
from django.urls import path

from .views import DashboardAPIKeyView
from .views import DashboardView

app_name = "dashboard"

urlpatterns = [
    path("", DashboardView.as_view(), name="home"),
    path("api-keys/", DashboardAPIKeyView.as_view(), name="api_key"),
    path("WhatsApp/", include("apps.dashboard.whatsapp.urls", namespace="whatsapp")),
]
