from chat.models import Chat, Message

from django.contrib import admin


@admin.register(Chat)
class ChatAdmin(admin.ModelAdmin):
    list_display = ('pk', 'create_date')
    fieldsets = (
        ('Users', {'fields': ('users', )}),
        ('Create', {'fields': ('create_date', )}),
    )


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('chat', 'user', 'body', 'send_date')
