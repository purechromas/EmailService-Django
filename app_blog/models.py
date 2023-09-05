from django.db import models


class Blog(models.Model):
    title = models.CharField(max_length=50, verbose_name='заголовок')
    blog = models.TextField(verbose_name='блог')
    image = models.ImageField(upload_to='blog/', verbose_name='изображение')
    quantity_views = models.IntegerField(default=0, verbose_name='количество просмотров')
    create_datetime = models.DateTimeField(auto_now_add=True, verbose_name='дата публикации')
    update_datetime = models.DateTimeField(auto_now=True, verbose_name='дата обновлении')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Блог'
        verbose_name_plural = 'Блоги'
