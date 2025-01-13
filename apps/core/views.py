from django.shortcuts import render

# Create your views here.
from django.views.generic import TemplateView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_not_required

from apps.mixins import UnAuthorizedTemplateMixin


@method_decorator(login_not_required, name="dispatch")
class HomeView(UnAuthorizedTemplateMixin):
    template_name = "pages/home.html"
