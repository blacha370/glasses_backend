from django.contrib import admin
from .models import ActiveOrder, UnactiveOrder

admin.site.register(ActiveOrder)
admin.site.register(UnactiveOrder)
