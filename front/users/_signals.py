import logging
from contextlib import suppress

from allauth.account.signals import user_signed_up
from allauth.socialaccount.signals import pre_social_login
from allauth.socialaccount.signals import social_account_added
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Profile
from .models import User

# Initialize the logger
logger = logging.getLogger(__name__)


@receiver(post_save, sender=User)
def create_or_update_profile(sender, instance, created, **kwargs):
    """
    Create or update a profile for the user when a User instance is saved.
    """
    if created:
        with suppress(Exception):
            Profile.objects.create(user=instance)

