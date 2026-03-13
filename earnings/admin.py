from django.contrib import admin
from .models import DriverEarning,Payout

# Register your models here.
@admin.register(DriverEarning)
class DriverEarningAdmin(admin.ModelAdmin):
    list_display = ('driver', 'shipment', 'earning_amount', 'is_paid', 'created_at')
@admin.register(Payout)
class PayoutAdmin(admin.ModelAdmin):
    list_display = ('driver', 'total_amount', 'payout_status', 'processed_at')
