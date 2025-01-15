from django.contrib import admin

from .models import Organization
from .models import Project


class ProjectInline(admin.StackedInline):
    model = Project
    extra = 0



@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "profile",
        "name",
        "hashed_name",
        "project_count",
        "created_at",
        "updated_at",
        "is_active",
        "is_archived",
        "is_archived_at",
    ]
    inlines = [ProjectInline]
