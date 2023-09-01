from django.db import models

from app_user.models import NULLABLE


class Client(models.Model):
    full_name = models.CharField(
        max_length=100,
        verbose_name='ФИО')
    email = models.EmailField(
        unique=False,
        verbose_name='почта')
    comment = models.TextField(
        **NULLABLE,
        verbose_name='комментарий')
    user = models.ForeignKey(
        to='app_user.User',
        on_delete=models.CASCADE,
        verbose_name='пользователь')
    mailings = models.ManyToManyField(
        to='app_email.Email',
        related_name='mailings',
        verbose_name='рассылки')

    def __str__(self):
        return self.full_name

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'
