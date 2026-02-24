from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import ListAPIView, RetrieveAPIView
from django.shortcuts import get_object_or_404
from .models import Shipment
from .serializers import ShipmentSerializer


STATUS_FLOW = [
    "Created",
    "Assigned",
    "Picked Up",
    "In Transit",
    "Out for Delivery",
    "Delivered"
]

FAILURE_STATUSES = ["Cancelled", "RTO", "Delivery Failed"]


# ✅ Create Shipment
class CreateShipmentAPIView(APIView):

    def post(self, request):
        serializer = ShipmentSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)

        return Response(serializer.errors, status=400)


# ✅ List + Search + Filter Shipments
class ListShipmentAPIView(ListAPIView):
    serializer_class = ShipmentSerializer

    def get_queryset(self):
        queryset = Shipment.objects.all()

        status_param = self.request.query_params.get('status')
        tracking_param = self.request.query_params.get('tracking')

        if status_param:
            queryset = queryset.filter(status=status_param)

        if tracking_param:
            queryset = queryset.filter(tracking_number__icontains=tracking_param)

        return queryset


# ✅ Bulk Create Shipments
class BulkCreateShipmentAPIView(APIView):

    def post(self, request):

        if not isinstance(request.data, list):
            return Response(
                {"error": "Expected a list of shipment objects"},
                status=400
            )

        serializer = ShipmentSerializer(data=request.data, many=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)

        return Response(serializer.errors, status=400)


# ✅ Assign Driver
class AssignDriverAPIView(APIView):

    def post(self, request, pk):
        shipment = get_object_or_404(Shipment, pk=pk)

        if shipment.status != "Created":
            return Response(
                {"error": "Driver can only be assigned when status is Created"},
                status=400
            )

        driver_name = request.data.get("driver_name")

        if not driver_name:
            return Response({"error": "driver_name is required"}, status=400)

        shipment.driver_name = driver_name
        shipment.status = "Assigned"
        shipment.save()

        return Response({"message": "Driver assigned successfully"}, status=200)


# ✅ Update Shipment Status
class UpdateShipmentStatusAPIView(APIView):

    def post(self, request, pk):

        shipment = get_object_or_404(Shipment, pk=pk)
        new_status = request.data.get("status")

        if not new_status:
            return Response({"error": "status is required"}, status=400)

        # ❌ Cannot modify delivered shipment
        if shipment.status == "Delivered":
            return Response(
                {"error": "Cannot update. Shipment already delivered."},
                status=400
            )

        # ❌ Cannot cancel after delivered
        if new_status == "Cancelled":
            if shipment.status == "Delivered":
                return Response(
                    {"error": "Cannot cancel delivered shipment"},
                    status=400
                )
            shipment.status = "Cancelled"
            shipment.save()
            return Response({"message": "Shipment Cancelled"}, status=200)

        # ✅ Delivery Failed
        if new_status == "Delivery Failed":
            shipment.status = "Delivery Failed"
            shipment.save()
            return Response({"message": "Shipment marked as Delivery Failed"}, status=200)

        # ✅ RTO
        if new_status == "RTO":
            shipment.status = "RTO"
            shipment.save()

            Shipment.objects.create(
                tracking_number=shipment.tracking_number + "-RTO",
                sender_name=shipment.receiver_name,
                receiver_name=shipment.sender_name,
                address=shipment.address,
                status="Created",
                is_reverse=True
            )

            return Response({"message": "RTO created with reverse shipment"}, status=200)

        # ✅ Normal Status Flow Validation
        try:
            current_index = STATUS_FLOW.index(shipment.status)
            new_index = STATUS_FLOW.index(new_status)
        except ValueError:
            return Response({"error": "Invalid status"}, status=400)

        if new_index != current_index + 1:
            return Response({"error": "Invalid status transition"}, status=400)

        shipment.status = new_status
        shipment.save()

        return Response({"message": "Status updated successfully"}, status=200)


# ✅ Shipment Detail API
class ShipmentDetailAPIView(RetrieveAPIView):
    queryset = Shipment.objects.all()
    serializer_class = ShipmentSerializer


# ✅ Bulk Update Status API
class BulkUpdateShipmentStatusAPIView(APIView):

    def post(self, request):

        shipment_ids = request.data.get("shipment_ids")
        new_status = request.data.get("status")

        if not shipment_ids or not isinstance(shipment_ids, list):
            return Response(
                {"error": "shipment_ids must be a list"},
                status=400
            )

        if not new_status:
            return Response(
                {"error": "status is required"},
                status=400
            )

        shipments = Shipment.objects.filter(id__in=shipment_ids)

        if not shipments.exists():
            return Response(
                {"error": "No shipments found"},
                status=404
            )

        updated_count = 0

        for shipment in shipments:

            # Skip delivered shipments
            if shipment.status == "Delivered":
                continue

            # Handle failure statuses
            if new_status in FAILURE_STATUSES:
                shipment.status = new_status
                shipment.save()
                updated_count += 1
                continue

            # Validate normal flow
            try:
                current_index = STATUS_FLOW.index(shipment.status)
                new_index = STATUS_FLOW.index(new_status)
            except ValueError:
                continue

            if new_index == current_index + 1:
                shipment.status = new_status
                shipment.save()
                updated_count += 1

        return Response(
            {"message": f"{updated_count} shipments updated successfully"},
            status=200
        )