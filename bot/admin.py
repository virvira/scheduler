from django.contrib import admin

from bot.models import TgUser


# Register your models here.
@admin.register(TgUser)
class TgUserAdmin(admin.ModelAdmin):
    list_display = ('chat_id', 'user')
    readonly_fields = ('verification_code', )
