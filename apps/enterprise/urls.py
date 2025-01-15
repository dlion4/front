from django.urls import path, include


app_name = "enterprise"

urlpatterns = [
    path("actions/", include("apps.enterprise.actions.urls", namespace="actions")),
]
