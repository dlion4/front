
from apps.mixins import DashboardTemplateMixin


# Create your views here.
class ProfileView(DashboardTemplateMixin):
    template_name = "profiles/home.html"
