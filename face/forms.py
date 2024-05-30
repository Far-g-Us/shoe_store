from django import forms
from face.models import Confirm


class ConfirmForm(forms.ModelForm):
    class Meta:
        model = Confirm
        fields = ['user']