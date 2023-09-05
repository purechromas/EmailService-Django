from random import sample

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.cache import cache
from django.views.generic import ListView

from app_blog.models import Blog
from app_client.models import Client
from app_email.models import Email


class MailingListView(LoginRequiredMixin, ListView):
    """This view is showing information about the user emails and 3 random blogs"""
    model = Email
    template_name = 'app_home/home.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)

        emails = Email.objects.filter(send_from_user=self.request.user)
        clients = Client.objects.filter(user=self.request.user)

        blogs = cache.get('all_blogs')
        if blogs is None:
            blogs = Blog.objects.all()
            cache.set('all_blogs', blogs, 60)

        active_emails = len([email for email in emails if email.status == 'Launched' or email.status == 'Created'])

        if blogs.count() >= 3:
            random_blogs = sample(list(blogs), 3)
        else:
            random_blogs = list(blogs)

        context['emails'] = emails
        context['total_emails'] = emails.count()
        context['active_emails'] = active_emails
        context['unique_clients'] = clients.count()
        context['blogs'] = random_blogs

        return context
