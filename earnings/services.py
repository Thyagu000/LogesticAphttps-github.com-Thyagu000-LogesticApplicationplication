from decimal import Decimal
from django.utils import timezone
from .models import DriverEarning,Payout

def claculate_driver_earning(shipment):
    
    delivery_fee = shipment.total_price
    commission_percentage = Decimal('10.0')
    commission = (delivery_fee * commission_percentage) / Decimal('100')
    driver_amount = delivery_fee - commission
    DriverEarning.objects.create(
        driver= shipment.driver,
        shipment=shipment,
        earning_amount= driver_amount,
        commission_amount = commission
    )
    
def process_payout(driver, earning_ids):
    earnings = DriverEarning.objects.filter(
        id__in=earning_ids,
        driver=driver,
        is_paid = False
    )
    
    total_amount = sum(e.earning_amount for e in earnings)
    
    payout = Payout.objects.create(
    driver=driver,
    total_amount=total_amount,
    payout_status='PROCESSING'
)
    
    earnings.update(
        payout=payout,
        is_paid = True
    )
    payout.payout_status='COMPLETED'
    payout.processed_at=timezone.now()
    payout.save()
    
    return payout