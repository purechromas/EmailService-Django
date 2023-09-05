from datetime import datetime, timedelta

from django.core.mail import send_mail

from app_email.models import Email
from app_log.models import EmailLog


def send_email(email):
    """This function is sending all crontab-jobs and also making logs with statistic"""
    try:
        send_mail(
            subject=email.subject,
            message=email.message,
            recipient_list=[client.email for client in email.send_to_client.all()],
            from_email=None
        )
        if email.frequency == 'Once':
            email.status = 'Finished'
        else:
            email.status = 'Launched'
        email.save()
    except Exception as error:
        email_log = EmailLog.objects.create(
            status='Failure', server_response=error, email=email)
        email_log.save()
    else:
        email_log = EmailLog.objects.create(
            status='Success', server_response='Sent successfully', email=email)
        email_log.save()


def cronjob():
    """This function is adding in crontab all emails so we can send them in proper time"""
    emails = Email.objects.filter(is_active=True, status__in=['Created', 'Launched']).exclude(status='Finished')
    cur_time = datetime.utcnow() + timedelta(hours=5)

    for email in emails:
        if email.status == 'Created':
            if email.frequency == 'Once':
                conditions_once(email, cur_time)
            elif email.frequency == 'Daily':
                conditions_daily(email, cur_time)
            elif email.frequency == 'Weekly':
                conditions_weekly(email, cur_time)
            elif email.frequency == 'Monthly':
                conditions_monthly(email, cur_time)
        elif email.status == 'Launched':
            if email.frequency == 'Daily':
                conditions_daily(email, cur_time)
            elif email.frequency == 'Weekly':
                conditions_weekly(email, cur_time)
            elif email.frequency == 'Monthly':
                conditions_monthly(email, cur_time)


def check_hour_minute(email, cur_time):
    if email.send_datetime.hour == cur_time.hour:
        if email.send_datetime.minute == cur_time.minute:
            send_email(email)


def conditions_once(email, cur_time):
    if email.send_datetime.day == cur_time.day:
        check_hour_minute(email, cur_time)


def conditions_daily(email, cur_time):
    check_hour_minute(email, cur_time)


def conditions_weekly(email, cur_time):
    if email.send_datetime.weekday() == cur_time.weekday():
        check_hour_minute(email, cur_time)


def conditions_monthly(email, cur_time):
    if email.send_datetime.day == cur_time.day:
        check_hour_minute(email, cur_time)
