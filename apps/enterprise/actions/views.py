from django.contrib.auth.decorators import login_not_required
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from apps.enterprise.forms import OrganizationForm


@require_POST
@csrf_exempt
def create_organization_view(request: HttpRequest):
    form = OrganizationForm(
        request.POST,
        profile=request.user.user_profile,
    )
    if form.is_valid():
        print(form.cleaned_data)
        instance = form.save()
        return JsonResponse(
            {
                "detail": "Organization Creation success",
                "url": request.build_absolute_uri(location=instance.get_absolute_url()),
            },
            status=200,
        )
    print(form.errors.get_json_data())
    return JsonResponse(form.errors.get_json_data(), status=400)
