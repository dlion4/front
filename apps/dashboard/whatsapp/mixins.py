from apps.mixins import DashboardTemplateMixin


class WhatsAppTemplateMixin(DashboardTemplateMixin):
    template_name = ""

    def get_template_names(self):
        return [self.template_name]
