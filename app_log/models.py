from django.db import models

from app_user.models import NULLABLE


class EmailLog(models.Model):
    class Status(models.TextChoices):
        SUCCESS = ('Success', 'Успешно')
        FAILURE = ('Failure', 'Не успешно')

    last_try_datetime = models.DateTimeField(
        auto_now=True,
        verbose_name='время последней попытки')
    status = models.CharField(
        max_length=25,
        choices=Status.choices,
        verbose_name='статус')
    server_response = models.TextField(
        **NULLABLE,
        verbose_name='ответ почтового сервера')
    email = models.OneToOneField(
        to='app_email.Email',
        on_delete=models.CASCADE,
        related_name='email_log'
    )

    def __str__(self):
        return f'Email status {self.status}, last try {self.last_try_datetime}.'

    class Meta:
        verbose_name = 'Логи рассылка'
        verbose_name_plural = 'Логи рассылки'
