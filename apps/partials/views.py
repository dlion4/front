from django.http.request import HttpRequest
from django.http.response import HttpResponse
from django.shortcuts import render

from apps.enterprise.whatsapp.forms import GroupForm


# Create your views here.
def get_load_onboarding_forms_view(request: HttpRequest)-> HttpResponse:
    path = request.GET.get("path", "organization")
    if path == "group":
        return render(
            request,
            "dashboard/components/modals/onboarding/forms/group.html",
            {"form": GroupForm()},
        )
    return render(
        request,
        "dashboard/components/modals/onboarding/forms/organization.html",
        {
            "form": None,
        },
    )
