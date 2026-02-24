from django.contrib import admin
from .models import Shipment


@admin.register(Shipment)
class ShipmentAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "tracking_number",
        "sender_name",
        "receiver_name",
        "status",
        "is_reverse",
        "created_at",
    )

    list_filter = (
        "status",
        "is_reverse",
        "created_at",
    )

    search_fields = (
        "tracking_number",
        "sender_name",
        "receiver_name",
    )

    ordering = ("-created_at",)

    readonly_fields = ("created_at", "updated_at")

    fieldsets = (
        ("Shipment Info", {
            "fields": (
                "tracking_number",
                "sender_name",
                "receiver_name",
                "address",
            )
        }),
        ("Status Info", {
            "fields": (
                "status",
                "is_reverse",
            )
        }),
        ("Timestamps", {
            "fields": (
                "created_at",
                "updated_at",
            )
        }),
    )