import contextlib
import json
import threading

from django.db import transaction
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from apps.enterprise.whatsapp.actions.helpers import whatsapp_group_member_lookup
from apps.enterprise.whatsapp.actions.helpers import whatsapp_member_lookup
from apps.enterprise.whatsapp.actions.threads import create_group_and_participants
from apps.enterprise.whatsapp.models import WhatsAppGroup
from apps.enterprise.whatsapp.models import WhatsAppGroupMessage
from apps.enterprise.whatsapp.models import WhatsAppMemberMessage


class WhatsAppMemberLookupView(View):
    def get(self, request, *args, **kwargs):
        return JsonResponse({}, status=200)


class WhatsAppGroupLookupView(View):
    def get(self, request, *args, **kwargs):
        group_id = request.GET.get("id", None)
        whatsapp_group = WhatsAppGroup.objects.filter(group_id=group_id)
        return JsonResponse({"group_exists": whatsapp_group.exists()}, status=200)


@method_decorator(csrf_exempt, name="dispatch")
@method_decorator(transaction.atomic, name="post")
class WhatsAppGroupCreateView(View):
    def post(self, request, *args, **kwargs):
        # with contextlib.suppress(json.JSONDecodeError):
        data = json.loads(request.body.decode("utf-8"))
        threading.Thread(target=create_group_and_participants, args=(data,)).start()
        return JsonResponse({}, status=201)


@method_decorator(csrf_exempt, name="dispatch")
@method_decorator(transaction.atomic, name="post")
class WhatsAppMemberCreateMessageView(View):
    def post(self, request, *args, **kwargs):
        with contextlib.suppress(json.JSONDecodeError):
            data = json.loads(request.body.decode("utf-8"))
            member = whatsapp_member_lookup(data)
            message = WhatsAppMemberMessage(
                remote_jid=data.get("remoteJid", ""),
                sender=member,
                message=data.get("message"),
                creation_date_str=data.get("timestamp"),
                message_id_str=data.get("id"),
                is_broadcast_message=data.get("broadcast", False),
                media_data=data.get("mediaData", {}),
            )
            message.save()
        return JsonResponse({}, status=201)


class WhatsAppGroupMessageCreateView(View):
    def post(self, request, *args, **kwargs):
        group_id = kwargs.get("group_id")
        with contextlib.suppress(json.JSONDecodeError, WhatsAppGroup.DoesNotExist):
            group = WhatsAppGroup.objects.get(group_id=group_id)
            data = json.loads(request.body.decode("utf-8"))
            member = whatsapp_group_member_lookup(data)
            message = WhatsAppGroupMessage(
                group=group,
                sender=member,
                message=data.get("message"),
                creation_date_str=data.get("timestamp"),
                message_id_str=data.get("id"),
                is_broadcast_message=data.get("broadcast", False),
                media_data=data.get("mediaData", {}),
            )
            message.save()
        return JsonResponse({}, status=201)

class WhatsAppMemberStatusSaveView(View):
    def post(self, request, *args, **kwargs):
        with contextlib.suppress(json.JSONDecodeError):
            data = json.loads(request.body.decode("utf-8"))
            member = whatsapp_group_member_lookup(data)
            message = WhatsAppMemberMessage(
                remote_jid=data.get("remoteJid"),
                sender=member,
                message=data.get("message"),
                creation_date_str=data.get("timestamp"),
                message_id_str=data.get("id"),
                is_broadcast_message=data.get("broadcast", False),
                media_data=data.get("mediaData", {}),
            )
            message.save()
        return JsonResponse({}, status=201)
