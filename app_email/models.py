from django.db import models

from app_user.models import NULLABLE


class Email(models.Model):
    FREQUENCY_CHOICES = [
        ('once', 'Единоразово'),
        ('daily', 'Ежедневно'),
        ('weekly', 'Еженедельно'),
        ('monthly', 'Ежемесячно'),
    ]

    STATUS_CHOICES = [
        ('created', 'создана'),
        ('launched', 'запушена'),
        ('finished', 'завершена'),
    ]

    subject = models.CharField(
        max_length=255,
        verbose_name='тема письма')
    message = models.TextField(
        verbose_name='сообщение')
    frequency = models.CharField(
        max_length=35,
        choices=FREQUENCY_CHOICES,
        verbose_name='частота')
    status = models.CharField(
        default=STATUS_CHOICES[0],
        max_length=35,
        choices=STATUS_CHOICES,
        verbose_name='статус')
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='время создания')
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='время обновления')
    send_time = models.TimeField(
        verbose_name='время отправление')
    send_day = models.DateField(
        verbose_name='дата отправление')
    send_from_user = models.ForeignKey(
        to='app_user.User',
        on_delete=models.CASCADE,
        related_name='user',
        verbose_name='отправитель')
    send_to_client = models.ManyToManyField(
        to='app_client.Client',
        related_name='client',
        verbose_name='получатель')

    def __str__(self):
        return f'Рассылка {self.subject})'

    class Meta:
        verbose_name = 'Рассылка'
        verbose_name_plural = 'Рассылки'
