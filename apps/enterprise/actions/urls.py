from django.urls import include
from django.urls import path

from . import views

app_name = "actions"

urlpatterns = [
    path(
        "organization/",
        include(
            [
                path(
                    "create/",
                    views.create_organization_view,
                    name="create_organization_view",
                ),
            ],
        ),
    ),
]
