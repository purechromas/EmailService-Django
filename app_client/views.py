from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DeleteView, UpdateView

from app_client.forms import ClientForm
from app_client.models import Client


class ClientListView(ListView):
    model = Client
    template_name = 'app_client/client_list.html'

    def get_queryset(self):
        clients = Client.objects.filter(user=self.request.user)
        return clients


class ClientCrateView(CreateView):
    model = Client
    form_class = ClientForm
    template_name = 'app_client/client_form.html'
    success_url = reverse_lazy('client:list')

    def form_valid(self, form):
        if form.is_valid():
            form.instance.user = self.request.user
        return super().form_valid(form)


class ClientUpdateView(UpdateView):
    model = Client
    form_class = ClientForm
    template_name = 'app_client/client_form.html'
    success_url = reverse_lazy('client:list')


class ClientDeleteView(DeleteView):
    model = Client
    template_name = 'app_client/client_confirm_delete.html'
    success_url = reverse_lazy('client:list')
