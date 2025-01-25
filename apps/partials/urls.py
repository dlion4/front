from django.urls import path
from . import views
app_name = "partials"
urlpatterns = [
    path(
        "load-onboarding-forms/",
        views.get_load_onboarding_forms_view,
        name="load_onboard_view",
    ),
]
