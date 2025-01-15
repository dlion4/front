from django.views.generic import TemplateView

from front.users.models import Profile

class UnAuthorizedTemplateMixin(TemplateView):
    template_name = ""
    def get_template_names(self):
        return [f"client/{self.template_name}"]


# Create your views here.
class DashboardTemplateMixin(TemplateView):
    template_ = "dashboard"
    template_name = None

    def get_template_names(self):
        return [
            f"{self.template_}/{self.template_name}",
        ]
    def get_profile(self) -> Profile|None:
        try:
            return self.request.user.user_profile
        except Profile.DoesNotExist:
            return None
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["profile"] = self.get_profile()
        return context
