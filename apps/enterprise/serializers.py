from rest_framework import serializers

from .models import Organization


class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = [
            "id",
            "name",
            "hashed_name",
            "project_count",
            "created_at",
            "updated_at",
            "is_active",
            "is_archived",
            "is_archived_at",
        ]
