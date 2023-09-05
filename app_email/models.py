from django.db import models
from app_user.models import NULLABLE


class Email(models.Model):
    class Frequency(models.TextChoices):
        ONCE = ('Once', 'Единоразово')
        DAILY = ('Daily', 'Ежедневно')
        WEEKLY = ('Weekly', 'Еженедельно')
        MONTHLY = ('Monthly', 'Ежемесячно')

    class Status(models.TextChoices):
        CREATED = ('Created', 'Создана')
        LAUNCHED = ('Launched', 'Запушена')
        FINISHED = ('Finished', ' Завершена')

    subject = models.CharField(
        max_length=255,
        verbose_name='тема письма')
    message = models.TextField(
        verbose_name='сообщение')
    frequency = models.CharField(
        max_length=35,
        choices=Frequency.choices,
        verbose_name='частота')
    status = models.CharField(
        default=Status.CREATED,
        max_length=30,
        choices=Status.choices,
        verbose_name='статус')
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='время создания')
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='время обновления')
    send_datetime = models.DateTimeField(
        **NULLABLE,
        verbose_name='время и дата отправление')
    send_from_user = models.ForeignKey(
        to='app_user.User',
        on_delete=models.CASCADE,
        related_name='user',
        verbose_name='отправитель')
    send_to_client = models.ManyToManyField(
        to='app_client.Client',
        related_name='client',
        verbose_name='получатель')
    is_active = models.BooleanField(
        default=True,
        verbose_name='активен')

    def __str__(self):
        return f'Рассылка {self.subject})'

    class Meta:
        verbose_name = 'Рассылка'
        verbose_name_plural = 'Рассылки'
