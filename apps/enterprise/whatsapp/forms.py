from django import forms

from apps.enterprise.whatsapp.models import Group


class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = [
            "group_name",
        ]
        widgets = {
            "group_name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Whatsapp Group Name",
                },
            ),
        }
