from django.urls import path
from .views import (
    ListCreateShipmentAPIView,
    ListShipmentAPIView,
    CreateShipmentAPIView,
    BulkCreateShipmentAPIView,
    AssignDriverAPIView,
    UpdateShipmentStatusAPIView,
    ShipmentDetailAPIView,
    BulkUpdateShipmentStatusAPIView,
)

urlpatterns = [
    # Create
    path("create/", CreateShipmentAPIView.as_view(), name="create-shipment"),
    path("bulk-create/", BulkCreateShipmentAPIView.as_view(), name="bulk-create-shipment"),

    # List
    path("", ListShipmentAPIView.as_view(), name="list-shipments"),

    # Detail
    path("<int:pk>/", ShipmentDetailAPIView.as_view(), name="shipment-detail"),

    # Actions
    path("<int:pk>/assign-driver/", AssignDriverAPIView.as_view(), name="assign-driver"),
    path("<int:pk>/update-status/", UpdateShipmentStatusAPIView.as_view(), name="update-status"),

    # Bulk Update
    path("bulk-update-status/", BulkUpdateShipmentStatusAPIView.as_view(), name="bulk-update-status"),
]