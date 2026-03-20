from django.shortcuts import render, get_object_or_404, redirect
from .models import TrackingLog, DeliveryAttempt
from shipments.models import Shipment
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

# Home page for tracking app
def index(request):
    return render(request, 'tracking/index.html')


# List of all shipments
def shipment_list(request):
    shipments = list(Shipment.objects.values())
    return JsonResponse(shipments, safe=False)


# Detail page for a single shipment
def shipment_detail(request, pk):
    shipment = Shipment.objects.get(pk=pk)

    data = {
        "id": str(shipment.id),
        "status": shipment.status
    }

    return JsonResponse(data)


# List of notifications (example: failed deliveries)
def notifications(request):
    delivery_attempts = DeliveryAttempt.objects.filter(is_rto=True).order_by('-timestamp')

    data = list(delivery_attempts.values(
        "id",
        "shipment_id",
        "attempt_number",
        "reason",
        "is_rto",
        "timestamp"
    ))

    return JsonResponse(data, safe=False)