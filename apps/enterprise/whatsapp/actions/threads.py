import contextlib

from django.db import IntegrityError

from apps.enterprise.whatsapp.models import WhatsAppGroup
from apps.enterprise.whatsapp.models import WhatsAppMember


def create_group_and_participants(data):
    with contextlib.suppress(IntegrityError, Exception):
        group = WhatsAppGroup.objects.create(
            group_id=data.get("id"),
            subject=data.get("subject"),
            subject_owner=data.get("subjectOwner"),
            size=data.get("size"),
            owner=data.get("owner"),
            creation_date_str=data.get("creation"),
            restrict=data.get("restrict"),
            announce=data.get("announce"),
            is_community=data.get("isCommunity"),
            is_community_announce=data.get("isCommunityAnnounce"),
            join_approval_mode=data.get("joinApprovalMode"),
            member_add_mode=data.get("memberAddMode"),
        )
        participants = [
            WhatsAppMember(
                member_id=participant.get("id"),
                push_name=participant.get("pushName") or "None",
                participant_id=participant.get("id"),
                admin=participant.get("admin") or "None",
                phone=participant.get("phone"),
            )
            for participant in data.get("participants")
        ]
        WhatsAppMember.objects.bulk_create(participants)
        group.participants.add(*participants)
