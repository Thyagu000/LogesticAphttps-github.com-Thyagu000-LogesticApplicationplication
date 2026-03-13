from django.views import View
from django.http import JsonResponse
from .models import DriverEarning, Payout

# List all earnings
class EarningsListView(View):
    def get(self, request):
        earnings = DriverEarning.objects.all().values(
            'id', 'driver_id', 'shipment_id', 'earning_amount', 'commission_amount', 'is_paid', 'created_at'
        )
        return JsonResponse(list(earnings), safe=False)

# Earnings for a specific driver
class DriverEarningsView(View):
    def get(self, request, driver_id):
        earnings = DriverEarning.objects.filter(driver_id=driver_id).values(
            'id', 'shipment_id', 'earning_amount', 'commission_amount', 'is_paid', 'created_at'
        )
        return JsonResponse(list(earnings), safe=False)

# List all payouts
class PayoutListView(View):
    def get(self, request):
        payouts = Payout.objects.all().values(
            'id', 'driver_id', 'total_amount', 'payout_status', 'refernce_id', 'created_at', 'processed_at'
        )
        return JsonResponse(list(payouts), safe=False)

# Payout detail
class PayoutDetailView(View):
    def get(self, request, id):
        try:
            payout = Payout.objects.filter(id=id).values(
                'id', 'driver_id', 'total_amount', 'payout_status', 'refernce_id', 'created_at', 'processed_at'
            ).first()
            if payout:
                return JsonResponse(payout)
            return JsonResponse({'error': 'Payout not found'}, status=404)
        except Payout.DoesNotExist:
            return JsonResponse({'error': 'Payout not found'}, status=404)

# Process payouts (example endpoint)
class PayoutProcessView(View):
    def post(self, request):
        # Example: Mark all pending payouts as processing
        pending_payouts = Payout.objects.filter(payout_status='PENDING')
        updated_count = pending_payouts.update(payout_status='PROCESSING')
        return JsonResponse({'message': f'{updated_count} payouts set to PROCESSING'})