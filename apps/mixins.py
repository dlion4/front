from django.views.generic import TemplateView

class UnAuthorizedTemplateMixin(TemplateView):
    template_name = ""
    def get_template_names(self):
        return [f"client/{self.template_name}"]
