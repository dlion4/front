from .mixins import DashboardTemplateMixin

class DashboardView(DashboardTemplateMixin):
    template_name = "pages/home.html"
