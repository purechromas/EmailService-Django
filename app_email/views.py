from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from app_email.forms import EmailForm
from app_email.models import Email
from app_email.services import cron_jobs_emails


class EmailListView(ListView):
    model = Email
    template_name = 'app_email/email_list.html'

    def get_queryset(self):
        """We are showing just mailings from the specific user id"""
        mailings = Email.objects.filter(send_from_user=self.request.user)
        return mailings


class EmailCreateView(CreateView):
    model = Email
    form_class = EmailForm
    template_name = 'app_email/email_form.html'
    success_url = reverse_lazy('email:list')

    def get_form_kwargs(self):
        """Sending user id to forms.py, so we can show only clients from this user."""
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        """Saving the E-mail with the user id from request"""
        if form.is_valid():
            form.instance.send_from_user = self.request.user
            form.save()
            cron_jobs_emails(form.instance)
        return super().form_valid(form)


class EmailUpdateView(UpdateView):
    model = Email
    form_class = EmailForm
    template_name = 'app_email/email_form.html'
    success_url = reverse_lazy('email:list')

    def get_form_kwargs(self):
        """Sending user id to forms.py, so we can show only clients from this user."""
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


class EmailDeleteView(DeleteView):
    model = Email
    template_name = 'app_email/email_confirm_delete.html'
    success_url = reverse_lazy('email:list')
