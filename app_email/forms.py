from datetime import datetime

from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone

from app_client.models import Client
from app_email.models import Email


class EmailForm(forms.ModelForm):
    class Meta:
        model = Email
        fields = ('subject', 'message', 'send_to_client', 'frequency', 'send_time', 'send_day')

        widgets = {
            'send_time': forms.TimeInput(
                attrs={"type": "time", "class": "form-control"}),
            'send_day': forms.DateInput(
                attrs={"type": "date", "class": "form-control"}),
        }

    def __init__(self, *args, **kwargs):
        # in CreateView we added user = self.request.user
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        if user:
            self.fields['send_to_client'].queryset = Client.objects.filter(user=user)

        self.fields['subject'].widget.attrs.update(
            {"class": "form-control", "placeholder": "Write email subject"})
        self.fields['message'].widget.attrs.update(
            {"class": "form-control", "rows": 5, "placeholder": "Write your message"})
        self.fields['frequency'].widget.attrs.update(
            {"class": "form-control"})
        self.fields['send_to_client'].widget.attrs.update(
            {"class": "form-control"})

        for field_name in self.fields:
            self.fields[field_name].label = ""
            self.fields[field_name].help_text = ""

    def clean_send_day(self):
        send_day = self.cleaned_data['send_day']
        if send_day < timezone.now().date():
            raise ValidationError("День отправки не может быть в прошлом")
        return send_day
