from django import forms

from apps.enterprise.whatsapp.models import WhatsAppGroup


class GroupForm(forms.ModelForm):
    class Meta:
        model = WhatsAppGroup
        fields = [
            "subject",
        ]
        widgets = {
            "subject": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Whatsapp Group Name",
                },
            ),
        }
