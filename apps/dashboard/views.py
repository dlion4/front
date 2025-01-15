
from apps.mixins import DashboardTemplateMixin


class DashboardView(DashboardTemplateMixin):
    template_name = "pages/home.html"
class DashboardAPIKeyView(DashboardTemplateMixin):
    template_name = "pages/api-keys.html"
