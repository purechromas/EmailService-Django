from django.contrib import admin

from app_client.models import Client


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    pass
