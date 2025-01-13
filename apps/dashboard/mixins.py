from django.views.generic import TemplateView
# Create your views here.
class DashboardTemplateMixin(TemplateView):
    template_ = "dashboard"
    template_name = None
    def get_template_names(self):
        return [f"{self.template_}/${self.template_name}"]