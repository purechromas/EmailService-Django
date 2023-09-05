from django.contrib import admin

from app_email.models import Email


@admin.register(Email)
class EmailAdmin(admin.ModelAdmin):
    moderator_fields = ('subject', 'message', 'frequency', 'status', 'send_datetime', 'send_from_user', 'send_to_client')

    def get_readonly_fields(self, request, obj=None):
        """This function is giving just a specific admin-rights on users witch are in group manager"""
        if request.user.groups.filter(name='manager').exists():
            return self.moderator_fields
        return super().get_readonly_fields(request, obj)
