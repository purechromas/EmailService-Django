from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.mail import send_mail
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from app_email.forms import EmailForm, ManagerEmailForm
from app_email.models import Email


class EmailListView(LoginRequiredMixin, ListView):
    model = Email
    template_name = 'app_email/email_list.html'
    permission_required = []

    def get_queryset(self):
        """Showing a specific emails according who is the request user"""
        if self.request.user.is_superuser or self.request.user.groups.filter(name='manager').exists():
            return Email.objects.all()
        return Email.objects.filter(send_from_user=self.request.user, is_active=True)


class EmailCreateView(LoginRequiredMixin, CreateView):
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
        return super().form_valid(form)


class EmailUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Email
    form_class = EmailForm
    template_name = 'app_email/email_form.html'
    success_url = reverse_lazy('email:list')
    permission_required = []

    def has_permission(self):
        """Giving permissions on specific request users"""
        email = self.get_object()
        if self.request.user == email.send_from_user or self.request.user.groups.filter(name='manager').exists():
            return super().has_permission()

    def get_form_kwargs(self):
        """Sending user id to forms.py, so we can show only clients from this user."""
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_form_class(self):
        """Showing a specific form according who is the request user"""
        if self.request.user == self.object.send_from_user:
            return EmailForm
        elif self.request.user.groups.filter(name='manager').exists():
            return ManagerEmailForm


class EmailDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Email
    template_name = 'app_email/email_confirm_delete.html'
    success_url = reverse_lazy('email:list')
    permission_required = []

    def has_permission(self):
        """Giving permissions on specific request users"""
        email = self.get_object()
        if self.request.user == email.send_from_user:
            return super().has_permission()
