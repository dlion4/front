from django.urls import path, include

app_name = "whatsapp"
urlpatterns = [
    path("actions/", include("apps.enterprise.whatsapp.actions.urls")),
]
