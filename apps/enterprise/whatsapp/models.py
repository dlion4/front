import uuid

from django.db import models

from front.users.models import Profile


class Group(models.Model):
    id = models.UUIDField(
        primary_key=True,
        unique=True,
        editable=False,
        default=uuid.uuid4,
        db_comment="Unique UUID for the Project",
    )
    group_name = models.CharField(max_length=255)
    creator = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        related_name="profile_group_profile",
    )
    members = models.ManyToManyField(Profile, related_name="groups")

    def __str__(self):
        return self.group_name

class GroupMessage(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    # Store sender's phone number or ID
    sender = models.CharField(max_length=255)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.sender}: {self.message}"


class GroupMembership(models.Model):
    group = models.ForeignKey(
        Group,
        on_delete=models.CASCADE,
        related_name="group_membership",
    )

    def __str__(self):
        return self.group.group_name

