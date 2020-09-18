from django.contrib import admin
from .models import ActiveOrder, UnactiveOrder, OrderStatusChange, MessagesThread, Message

admin.site.register(ActiveOrder)
admin.site.register(UnactiveOrder)
admin.site.register(OrderStatusChange)
admin.site.register(MessagesThread)
admin.site.register(Message)
