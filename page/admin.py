from django.contrib import admin
from .models import ActiveOrder, OrderStatusChange, MessagesThread, Message, Notification

admin.site.register(ActiveOrder)
admin.site.register(OrderStatusChange)
admin.site.register(MessagesThread)
admin.site.register(Message)
admin.site.register(Notification)
