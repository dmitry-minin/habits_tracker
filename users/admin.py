from django.contrib import admin

from users.models import User

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("email", "tg_chat_id")
    search_fields = ("email", "tg_chat_id")
    ordering = ("email",)