from django.urls import path

from . import views

# /enterprise/whatsapp/actions/
urlpatterns = [
    path("member-lookup/", views.WhatsAppMemberLookupView.as_view()),
    path("group-lookup/", views.WhatsAppGroupLookupView.as_view()),
    path("group-create/", views.WhatsAppGroupCreateView.as_view()),
    path(
        "group-create/<group_id>/message/",
        views.WhatsAppGroupMessageCreateView.as_view(),
    ),
    path("messages/create/", views.WhatsAppMemberCreateMessageView.as_view()),
    path("status/create/", views.WhatsAppMemberStatusSaveView.as_view()),
]
