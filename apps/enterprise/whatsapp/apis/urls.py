from django.urls import include
from django.urls import path

from . import websockets as views

# /api/whatsapp/messages/received/
urlpatterns = [
    path("messages/", views.ReceiveMessageView.as_view()),
]
