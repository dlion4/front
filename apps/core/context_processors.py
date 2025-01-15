from apps.enterprise.forms import OrganizationForm


def core_context_processor_data(request):
    if request.user.is_authenticated:
        profile = request.user.user_profile
        return {"organization_from": OrganizationForm(profile=profile)}
    return {}
