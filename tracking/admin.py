from django.contrib import admin
from .models import TrackingLog, DeliveryAttempt

@admin.register(TrackingLog)
class TrackingLogAdmin(admin.ModelAdmin):
    list_display = ('shipment', 'status', 'updated_by', 'timestamp')
    list_filter = ('status', 'timestamp')
    search_fields = ('shipment__id', 'status', 'updated_by__email')
    readonly_fields = ('timestamp',)
    ordering = ('-timestamp',)


@admin.register(DeliveryAttempt)
class DeliveryAttemptAdmin(admin.ModelAdmin):
    list_display = ('shipment', 'attempt_number', 'attempted_by', 'is_rto', 'timestamp')
    list_filter = ('is_rto', 'timestamp')
    search_fields = ('shipment__id', 'attempted_by__email', 'reason')
    readonly_fields = ('timestamp', 'attempt_number', 'is_rto')
    ordering = ('shipment', 'attempt_number')