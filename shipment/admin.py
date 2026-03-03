from django.contrib import admin
from .models import Shipment, Parcel

class ParcelInline(admin.TabularInline):
    model = Parcel
    extra = 1

@admin.register(Shipment)
class ShipmentAdmin(admin.ModelAdmin):
    inlines = [ParcelInline]

@admin.register(Parcel)
class ParcelAdmin(admin.ModelAdmin):
    list_display = ('shipment', 'weight', 'description')