from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from .models import Shipment
from .serializers import ShipmentSerializer
from drivers.models import DriverProfile


STATUS_FLOW = [
    "Created", "Assigned", "Picked Up", "In Transit", "Out for Delivery", "Delivered"
]

FAILURE_STATUSES = ["Cancelled", "RTO", "Delivery Failed"]


# ✅ Create Shipment
class CreateShipmentAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ShipmentSerializer(data=request.data)

        if serializer.is_valid():

            if request.user.is_superuser:
                serializer.save(customer=request.user)
            else:
                serializer.save(
                    tenant=request.user.tenant,
                    customer=request.user
                )

            return Response(serializer.data, status=201)

        return Response(serializer.errors, status=400)


# ✅ List + Search + Filter Shipments
class ListShipmentAPIView(ListAPIView):

    serializer_class = ShipmentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        if user.is_superuser:
            queryset = Shipment.objects.filter(is_deleted=False)
        else:
            queryset = Shipment.objects.filter(
                tenant=user.tenant,
                is_deleted=False
            )

        status_param = self.request.query_params.get('status')
        tracking_param = self.request.query_params.get('tracking')
        order_param = self.request.query_params.get('order_number')

        if status_param:
            queryset = queryset.filter(status=status_param)

        if tracking_param:
            queryset = queryset.filter(tracking_number__icontains=tracking_param)

        if order_param:
            queryset = queryset.filter(order_number__icontains=order_param)

        return queryset


# ✅ Assign Driver (Fixed to use FK)
class AssignDriverAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request, pk):

        user = request.user

        if user.is_superuser:
            shipment = get_object_or_404(Shipment, pk=pk, is_deleted=False)
        else:
            shipment = get_object_or_404(
                Shipment,
                pk=pk,
                tenant=user.tenant,
                is_deleted=False
            )

        if shipment.status != "Created":
            return Response({"error": "Driver can only be assigned when status is Created"}, status=400)

        driver_id = request.data.get("driver_id")

        if not driver_id:
            return Response({"error": "driver_id is required"}, status=400)

        driver = get_object_or_404(DriverProfile, id=driver_id)

        shipment.driver = driver
        shipment.status = "Assigned"
        shipment.save()

        return Response({"message": "Driver assigned successfully"}, status=200)


# ✅ Update Shipment Status
class UpdateShipmentStatusAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request, pk):

        user = request.user

        if user.is_superuser:
            shipment = get_object_or_404(Shipment, pk=pk, is_deleted=False)
        else:
            shipment = get_object_or_404(
                Shipment,
                pk=pk,
                tenant=user.tenant,
                is_deleted=False
            )

        new_status = request.data.get("status")

        if not new_status:
            return Response({"error": "status is required"}, status=400)

        if shipment.status == "Delivered":
            return Response(
                {"error": "Cannot update. Shipment already delivered."},
                status=400
            )

        # Failure statuses
        if new_status in FAILURE_STATUSES:
            shipment.status = new_status
            shipment.save()

            # Create reverse shipment for RTO
            if new_status == "RTO":
                Shipment.objects.create(
                    tenant=shipment.tenant,
                    customer=shipment.customer,
                    order_number=shipment.order_number + "-RTO",
                    tracking_number=(shipment.tracking_number or "") + "-RTO",
                    sender_name=shipment.receiver_name,
                    receiver_name=shipment.sender_name,
                    address=shipment.address,
                    status="Created",
                    is_reverse=True
                )

            return Response({"message": f"Shipment marked as {new_status}"}, status=200)

        # Normal flow validation
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

    serializer_class = ShipmentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        if user.is_superuser:
            return Shipment.objects.filter(is_deleted=False)

        return Shipment.objects.filter(
            tenant=user.tenant,
            is_deleted=False
        )

# ✅ Bulk Create Shipments
class BulkCreateShipmentAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):

        if not isinstance(request.data, list):
            return Response(
                {"error": "Expected a list of shipment objects"},
                status=400
            )

        serializer = ShipmentSerializer(data=request.data, many=True)

        if serializer.is_valid():
            if request.user.is_superuser:
                serializer.save()
            else:
                serializer.save(tenant=request.user.tenant)

            return Response(serializer.data, status=201)

        return Response(serializer.errors, status=400)


# ✅ Bulk Update Status API
class BulkUpdateShipmentStatusAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):
        shipment_ids = request.data.get("shipment_ids")
        new_status = request.data.get("status")
        user = request.user

        if not shipment_ids or not isinstance(shipment_ids, list):
            return Response({"error": "shipment_ids must be a list"}, status=400)

        if not new_status:
            return Response({"error": "status is required"}, status=400)

        if user.is_superuser:
            shipments = Shipment.objects.filter(id__in=shipment_ids, is_deleted=False)
        else:
            shipments = Shipment.objects.filter(
                id__in=shipment_ids,
                tenant=user.tenant,
                is_deleted=False
            )

        updated_count = 0
        for shipment in shipments:

            if shipment.status == "Delivered":
                continue

            if new_status in FAILURE_STATUSES:
                shipment.status = new_status
                shipment.save()
                updated_count += 1
                continue

            try:
                current_index = STATUS_FLOW.index(shipment.status)
                new_index = STATUS_FLOW.index(new_status)
                if new_index == current_index + 1:
                    shipment.status = new_status
                    shipment.save()
                    updated_count += 1
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