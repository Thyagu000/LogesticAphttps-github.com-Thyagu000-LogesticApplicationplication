from django.contrib import admin
from .models import Item, Receiver, Shipment

admin.site.register(Item)
admin.site.register(Receiver)
admin.site.register(Shipment)