from django.contrib import admin
from .models import Payment

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'shipment_id',
        'payer_id',
        'amount',
        'payment_method',
        'payment_status',
        'created_at',
    )
    