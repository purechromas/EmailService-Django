from django.core.management import BaseCommand

from app_email.services import cronjob


class Command(BaseCommand):
    def handle(self, *args, **options):
        cronjob()
