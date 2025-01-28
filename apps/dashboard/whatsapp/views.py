from django.views.generic import TemplateView

from apps.dashboard.whatsapp.mixins import WhatsAppTemplateMixin


class HomeView(WhatsAppTemplateMixin):
    template_name = "whatsapp/home.html"


home = HomeView.as_view()
