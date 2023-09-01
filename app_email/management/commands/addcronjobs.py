from django.core.mail import send_mail
from django.core.management import BaseCommand

from app_email.models import Email


class Command(BaseCommand):
    def handle(self, *args, **options):
        emails = Email.objects.all()

        for email in emails:
            if email.frequency == 'once':
                try:
                    self._send_email(email)
                except Exception as error:
                    print(error)
                else:
                    email.status = 'finished'
                    email.save()

    @staticmethod
    def _send_email(email: Email) -> None:
        send_mail(
            subject=email.subject,
            message=email.message,
            recipient_list=[client for client in email.send_to_client.all()],
            from_email=None
        )
