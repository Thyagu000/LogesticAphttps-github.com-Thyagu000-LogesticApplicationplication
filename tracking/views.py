from rest_framework import viewsets
from .models import ShipmentTracking, DeliveryAttempt
from .serializers import ShipmentTrackingSerializer, DeliveryAttemptSerializer
from shipments.models import Shipment
from rest_framework.response import Response
from rest_framework.decorators import action

class ShipmentTrackingViewSet(viewsets.ModelViewSet):
    queryset = ShipmentTracking.objects.all()
    serializer_class = ShipmentTrackingSerializer

class DeliveryAttemptViewSet(viewsets.ModelViewSet):
    queryset = DeliveryAttempt.objects.all()
    serializer_class = DeliveryAttemptSerializer

    @action(detail=True, methods=["post"])
    def record_attempt(self, request, pk=None):
        shipment = Shipment.objects.get(pk=pk)
        max_attempts = 3
        attempts_count = shipment.delivery_attempts.count() + 1

        status = request.data.get("status")
        remarks = request.data.get("remarks")
        proof = request.FILES.get("proof_image")

        attempt = DeliveryAttempt.objects.create(
            shipment=shipment,
            attempt_number=attempts_count,
            status=status,
            remarks=remarks,
            proof_image=proof
        )

        # Auto-mark RTO if max attempts reached
        if attempts_count >= max_attempts:
            shipment.current_status = "RTO"
            shipment.save()

        return Response({"message": "Delivery attempt recorded", "attempt_number": attempt.attempt_number})