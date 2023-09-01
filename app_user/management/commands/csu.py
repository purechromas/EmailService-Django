from django.core.management import BaseCommand

from app_user.models import User


class Command(BaseCommand):
    def handle(self, *args, **options):
        user = User.objects.create(
            email='superuser@gmail.com',
            is_active=True,
            is_staff=True,
            is_superuser=True
        )

        user.set_password('superuser')
        user.save()
