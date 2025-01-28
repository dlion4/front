from django.conf import settings
from django.http import JsonResponse
from django.middleware.csrf import get_token
from django.urls import include
from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework.routers import SimpleRouter

from front.users.api.views import UserViewSet

router = DefaultRouter() if settings.DEBUG else SimpleRouter()

router.register("users", UserViewSet)



def generate_csrf_token(request):
    csrf_token = get_token(request)
    return JsonResponse({"csrfToken": csrf_token})


app_name = "api"
urlpatterns = [
    *router.urls,
    path("whatsapp/", include("apps.enterprise.whatsapp.apis.urls")),
    path("csrf-token/", generate_csrf_token, name="generate_csrf_token"),
]
