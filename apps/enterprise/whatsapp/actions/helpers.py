from django.db.models import Q

from apps.enterprise.whatsapp.models import WhatsAppMember


def retrieve_phone_from_remote_jid(remote_jid)-> str:
    return remote_jid[:remote_jid.index("@")]


def whatsapp_member_lookup(data) -> WhatsAppMember:
    #  will improve this to avoid duplication later
    lookup_id = data.get("remoteJid")
    member_filter = WhatsAppMember.objects.filter(
        Q(member_id=lookup_id) | Q(participant_id=lookup_id),
    )
    if not member_filter.exists():
        return WhatsAppMember.objects.create(
            member_id=data.get("remoteJid"),
            push_name=data.get("author") or "None",
            participant_id=data.get("id"),
            admin="None",
            phone=retrieve_phone_from_remote_jid(data.get("remoteJid")),
        )
    return member_filter.first()

def whatsapp_group_member_lookup(data)-> WhatsAppMember:
    #  will improve this to avoid duplication later
    lookup_id = data.get("participant")
    member_filter = WhatsAppMember.objects.filter(
        Q(member_id=lookup_id) | Q(participant_id=lookup_id),
    )
    if not member_filter.exists():
        return WhatsAppMember.objects.create(
            member_id=data.get("participant"),
            push_name=data.get("author") or "None",
            participant_id=data.get("participant"),
            admin="None",
            phone=retrieve_phone_from_remote_jid(data.get("participant")),
        )
    return member_filter.first()
