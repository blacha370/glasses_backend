from django.contrib import admin
from .models import ActiveOrder, UnactiveOrder, OrderStatusChange, MessagesThread, Message, Notification, ArchiveThread, ArchiveMessage

admin.site.register(ActiveOrder)
admin.site.register(UnactiveOrder)
admin.site.register(OrderStatusChange)
admin.site.register(MessagesThread)
admin.site.register(Message)
admin.site.register(Notification)
admin.site.register(ArchiveThread)
admin.site.register(ArchiveMessage)
