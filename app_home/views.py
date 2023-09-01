from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView

from app_email.models import Email


class MailingListView(LoginRequiredMixin, ListView):
    model = Email
    template_name = 'app_home/home.html'

    def get_queryset(self):
        mailings = Email.objects.filter(send_from_user=self.request.user)
        return mailings
