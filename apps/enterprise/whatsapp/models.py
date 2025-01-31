import uuid
from datetime import datetime

from django.db import models

from apps.enterprise.whatsapp._abstracts import BaseMessageModel
from front.users.models import Profile


class WhatsAppMember(models.Model):
    id = models.UUIDField(
        primary_key=True,
        unique=True,
        editable=False,
        default=uuid.uuid4,
    )
    profile = models.OneToOneField(
        Profile,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="profile_whatsapp_member",
    )
    member_id = models.CharField(max_length=100, blank=True)
    push_name = models.CharField(max_length=100, blank=True, default="None")
    participant_id = models.CharField(max_length=255)
    admin = models.CharField(max_length=50, blank=True, default="None")
    phone = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.push_name}".title()


class WhatsAppMemberMessage(BaseMessageModel):
    remote_jid = models.CharField(default="status@broadcast", max_length=300)
    member = models.ForeignKey(
        WhatsAppMember,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="member_message_recipient",
    )
    sender = models.ForeignKey(
        WhatsAppMember,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="member_message_sender",
    )
    creation_date_str = models.CharField(max_length=200, blank=True)
    is_broadcast_message = models.BooleanField(default=False)


class WhatsAppGroup(models.Model):
    id = models.UUIDField(
        primary_key=True,
        unique=True,
        editable=False,
        default=uuid.uuid4,
    )
    group_id = models.CharField(max_length=300, unique=True)
    subject = models.CharField(max_length=255)
    subject_owner = models.CharField(max_length=255)
    subject_time = models.BigIntegerField(default=12298)
    size = models.IntegerField(default=1)
    data_created_on_whatsapp_cloud = models.DateTimeField(blank=True, null=True)
    owner = models.CharField(max_length=255)
    restrict = models.BooleanField(default=False)
    announce = models.BooleanField(default=False)
    is_community = models.BooleanField(default=False)
    is_community_announce = models.BooleanField(default=False)
    join_approval_mode = models.BooleanField(default=False)
    member_add_mode = models.BooleanField(default=True)
    participants = models.ManyToManyField(
        WhatsAppMember, blank=True, related_name="whatsapp_group_participants",
    )
    creation_date_str = models.CharField(blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.set_creation_date(self.creation_date_str)
        super().save(*args, **kwargs)

    @property
    def name(self):
        return self.subject

    def set_creation_date(self, creation_date_str):
        """Convert creationDate string to datetime and save it"""
        if creation_date_str:
            self.data_created_on_whatsapp_cloud = datetime.strptime(  # noqa: DTZ007
                creation_date_str, "%m/%d/%Y, %I:%M:%S %p",
            )


class WhatsAppGroupMessage(BaseMessageModel):
    group = models.ForeignKey(
        WhatsAppGroup,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    sender = models.ForeignKey(
        WhatsAppMember,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="group_sender_message",
    )
    creation_date_str = models.CharField(max_length=200, blank=True)
    is_broadcast_message = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.sender}: {self.message}"


class NotificationSubscription(models.Model):
    whatsapp_groups = models.ManyToManyField(
        WhatsAppGroup,
        blank=True,
        related_name="notification_subscriptions",
    )
    whatsapp_members = models.ManyToManyField(
        WhatsAppMember,
        blank=True,
        related_name="notification_subscriptions",
    )
    notification_channel = models.CharField(
        max_length=255,
        choices=[
            ("EMAIL", "Email"),
            ("SMS", "SMS"),
            ("WHATSAPP", "WhatsApp"),
        ],
        default="SMS",
        blank=False,
        null=False,
        db_index=True,
    )

    def __str__(self):
        return f"Notification Subscription: {self.notification_channel}"
