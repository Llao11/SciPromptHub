from django import forms
from .models import Prompt, Tag


class PromptForm(forms.ModelForm):
    tags_input = forms.CharField(
        required=False, help_text="Comma-separated tags", max_length=100
    )

    class Meta:
        model = Prompt
        fields = ["name", "text", "description", "tags"]
        widgets = {
            "name": forms.TextInput(attrs={"style": "height: 50%;"}),
        }
