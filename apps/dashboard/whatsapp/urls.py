from django.urls import path
from .views import home

app_name = "whatsapp"
urlpatterns = [path("", home, name="home")]
