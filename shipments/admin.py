from django.contrib import admin
from .models import Shipment


@admin.register(Shipment)
class ShipmentAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "order_number",
        "tracking_number",
        "status",
        "tenant",
        "is_deleted",
        "created_at",
    )

    list_filter = (
        "status",
        "tenant",
        "is_deleted",
    )

    search_fields = (
        "order_number",
        "tracking_number",
        "sender_name",
        "receiver_name",
    )

    ordering = ("-created_at",)