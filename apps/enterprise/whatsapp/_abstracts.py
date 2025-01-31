from datetime import datetime

from django.db import models


class BaseMessageModel(models.Model):
    message = models.JSONField()
    timestamp = models.DateTimeField(auto_now_add=True)
    message_id_str = models.CharField(max_length=500, blank=True)
    media_data = models.JSONField(blank=True, null=True)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        self.set_creation_date(self.creation_date_str)
        super().save(*args, **kwargs)

    def set_creation_date(self, creation_date_str):
        """Convert creationDate string to datetime and save it"""
        if creation_date_str:
            self.timestamp = datetime.strptime(  # noqa: DTZ007
                creation_date_str, "%m/%d/%Y, %I:%M:%S %p",
            )
