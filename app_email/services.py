from django.conf import settings
from django.core.mail import send_mail
from django.core.management import call_command


def send_email(email) -> None:
    try:
        send_mail(
            subject=email['subject'],
            message=email['message'],
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=email['recipient_list']
        )
    except Exception as e:
        print(e)


def cron_jobs_emails(obj):
    clients = obj.send_to_client.all()
    cron_mail = {
        'subject': obj.subject,
        'message': obj.message,
        'recipient_list': [client.email for client in clients]
    }
    hour, minute = obj.send_time.strftime("%H:%M").split(":")

    if obj.frequency == 'once':
        cron_schedule = f'{minute} {hour} {obj.send_day.day} {obj.send_day.month} *'
        cron_function_path = f'app_email.services.send_email'

        cronjob = (cron_schedule, cron_function_path, [cron_mail])
        print(cronjob)
        settings.CRONJOBS.append(cronjob)
        print(settings.CRONJOBS)
        call_command('crontab', 'remove')
        call_command('crontab', 'add')
        call_command('crontab', 'show')
