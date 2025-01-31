from django.urls import include
from django.urls import path

app_name = "enterprise"

urlpatterns = [
    path("actions/", include("apps.enterprise.actions.urls", namespace="actions")),
    path("whatsapp/", include("apps.enterprise.whatsapp.urls", namespace="whatsapp")),
]
